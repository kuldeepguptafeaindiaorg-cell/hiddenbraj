import csv
import json
import logging
from datetime import date, timedelta

import requests
from django.conf import settings
from django.core.mail import send_mail
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    JsonResponse,
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm
from .models import Registration

logger = logging.getLogger(__name__)


# ─── Helpers ────────────────────────────────────────────────────────────────

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def send_notification_email(registration):
    """Send an alert email to ADMIN_EMAIL when a new registration arrives."""
    if not (settings.EMAIL_HOST_USER and settings.ADMIN_EMAIL):
        return
    try:
        subject = f"[HiddenBraj] New registration — {registration.name}"
        body = (
            f"Name:      {registration.name}\n"
            f"Phone:     {registration.phone}\n"
            f"Email:     {registration.email or '—'}\n"
            f"City:      {registration.city or '—'}\n"
            f"Tour type: {registration.get_tour_type_display() or '—'}\n"
            f"Message:   {registration.message or '—'}\n"
            f"Registered at: {registration.created_at}\n"
        )
        send_mail(subject, body, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL])
    except Exception as exc:
        logger.warning("Email notification failed: %s", exc)


def send_whatsapp_notification(registration):
    """Send a WhatsApp alert to admin via CallMeBot when a new registration arrives.

    One-time setup:
      1. Save +34 644 56 78 10 in your contacts as "CallMeBot"
      2. Send this message on WhatsApp: I allow callmebot to send me messages
      3. You'll receive your API key via WhatsApp
      4. Set env vars: WHATSAPP_NUMBER (with country code, e.g. 919876543210)
                       WHATSAPP_API_KEY (received from CallMeBot)
    """
    phone  = getattr(settings, 'WHATSAPP_NUMBER', '')
    apikey = getattr(settings, 'WHATSAPP_API_KEY', '')
    if not (phone and apikey):
        return
    try:
        now_ist = registration.created_at.astimezone(
            __import__('zoneinfo').ZoneInfo('Asia/Kolkata')
        ).strftime('%d %b %Y, %I:%M %p IST')
        text = (
            f"🪔 *HiddenBraj — Naya Registration!*\n\n"
            f"👤 *Naam:* {registration.name}\n"
            f"📞 *Phone:* {registration.phone}\n"
            f"📧 *Email:* {registration.email or '—'}\n"
            f"🏙️ *Shahar:* {registration.city or '—'}\n"
            f"🗺️ *Tour:* {registration.get_tour_type_display() or '—'}\n"
            f"💬 *Sandesh:* {registration.message or '—'}\n"
            f"🕐 *Samay:* {now_ist}"
        )
        import urllib.parse
        url = (
            f"https://api.callmebot.com/whatsapp.php"
            f"?phone={phone}&text={urllib.parse.quote(text)}&apikey={apikey}"
        )
        resp = requests.get(url, timeout=8)
        if resp.status_code != 200:
            logger.warning("WhatsApp notification failed (status %s): %s", resp.status_code, resp.text[:200])
    except Exception as exc:
        logger.warning("WhatsApp notification error: %s", exc)


def push_to_google_sheet(registration):
    """POST registration data to a Google Apps Script webhook if configured."""
    webhook = getattr(settings, 'GOOGLE_SHEET_WEBHOOK', '')
    if not webhook:
        return
    payload = {
        'id':        registration.id,
        'ts':        registration.created_at.isoformat(),
        'name':      registration.name,
        'phone':     registration.phone,
        'email':     registration.email,
        'city':      registration.city,
        'tourType':  registration.tour_type,
        'message':   registration.message,
    }
    try:
        requests.post(webhook, json=payload, timeout=5)
    except Exception as exc:
        logger.warning("Google Sheet push failed: %s", exc)


# ─── API: POST /api/register ─────────────────────────────────────────────────

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    """
    Accepts JSON or form-encoded POST from the website's registration form.
    Returns JSON { success, message, id }.
    """

    def post(self, request):
        content_type = request.content_type or ''

        if 'application/json' in content_type:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
        else:
            data = request.POST

        form = RegistrationForm(data)
        if not form.is_valid():
            return JsonResponse(
                {'success': False, 'message': 'Validation error', 'errors': form.errors},
                status=422,
            )

        registration = form.save(commit=False)
        registration.ip_address = get_client_ip(request)
        registration.save()

        # Side-effects (fire and forget — failures are logged, not raised)
        send_notification_email(registration)
        send_whatsapp_notification(registration)
        push_to_google_sheet(registration)

        return JsonResponse(
            {
                'success': True,
                'message': 'Registration successful! We will contact you soon.',
                'id': registration.id,
            },
            status=201,
        )

    def get(self, request):
        return JsonResponse({'detail': 'Method not allowed'}, status=405)


# ─── API: GET /api/stats (public) ────────────────────────────────────────────

class StatsView(View):
    """Returns public registration count — no auth required."""

    def get(self, request):
        count = Registration.objects.count()
        return JsonResponse({'registrations': count})


# ─── API: GET /api/admin-registrations ──────────────────────────────────────

class AdminRegistrationsView(View):
    """
    Returns all registrations as JSON, protected by a bearer / query token.
    Usage:
        GET /api/admin-registrations
        Authorization: Bearer <ADMIN_TOKEN>
        — or —
        GET /api/admin-registrations?token=<ADMIN_TOKEN>
    """

    def _check_auth(self, request):
        token = getattr(settings, 'ADMIN_TOKEN', '')
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        bearer = auth_header.removeprefix('Bearer ').strip()
        query_token = request.GET.get('token', '')
        return bearer == token or query_token == token

    def get(self, request):
        if not self._check_auth(request):
            return JsonResponse({'detail': 'Forbidden'}, status=403)

        registrations = Registration.objects.all()

        today = date.today()
        total = registrations.count()
        today_count = registrations.filter(created_at__date=today).count()
        tour_count = registrations.exclude(tour_type='').count()

        data = [
            {
                'id':        r.id,
                'ts':        r.created_at.isoformat(),
                'name':      r.name,
                'phone':     r.phone,
                'email':     r.email,
                'city':      r.city,
                'tourType':  r.tour_type,
                'tourLabel': r.get_tour_type_display(),
                'message':   r.message,
            }
            for r in registrations
        ]

        return JsonResponse(
            {
                'stats': {
                    'total':   total,
                    'today':   today_count,
                    'tours':   tour_count,
                },
                'registrations': data,
            }
        )


# ─── CSV Export ──────────────────────────────────────────────────────────────

class AdminExportCSVView(View):
    """Download all registrations as a CSV file."""

    def _check_auth(self, request):
        token = getattr(settings, 'ADMIN_TOKEN', '')
        return request.GET.get('token', '') == token

    def get(self, request):
        if not self._check_auth(request):
            return HttpResponseForbidden('Forbidden')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="hiddenbraj_registrations.csv"'
        response.write('\ufeff')  # UTF-8 BOM for Excel compatibility

        writer = csv.writer(response)
        writer.writerow(['ID', 'Registered At', 'Name', 'Phone', 'Email', 'City', 'Tour Type', 'Message'])

        for r in Registration.objects.all():
            writer.writerow([
                r.id,
                r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                r.name,
                r.phone,
                r.email,
                r.city,
                r.get_tour_type_display(),
                r.message,
            ])

        return response


# ─── Admin Panel (HTML) ───────────────────────────────────────────────────────

class AdminPanelView(View):
    """Serves the standalone admin panel HTML page."""

    def get(self, request):
        # The HTML admin panel authenticates via JS using the /api/admin-registrations endpoint
        from django.template.loader import render_to_string
        content = render_to_string('admin/index.html', request=request)
        return HttpResponse(content, content_type='text/html')
