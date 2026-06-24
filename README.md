# 🪔 HiddenBraj — Django Backend

Full Django backend for the HiddenBraj "Sampurna Braj Darshan" website.

---

## 📁 Project Structure

```
hiddenbraj/
├── hiddenbraj/           ← Django project package
│   ├── settings.py       ← All configuration
│   ├── urls.py           ← Root URL router
│   └── wsgi.py           ← WSGI entry point
├── registrations/        ← Main Django app
│   ├── models.py         ← Registration model (DB table)
│   ├── forms.py          ← Form validation
│   ├── views.py          ← API + admin views
│   ├── urls.py           ← App-level URL patterns
│   ├── admin.py          ← Django admin site config
│   └── migrations/       ← Database migrations
├── templates/
│   ├── index.html        ← Main website (your HTML, patched for Django)
│   └── admin/
│       └── index.html    ← Custom admin panel
├── static/               ← Static files (CSS, images, etc.)
├── manage.py
├── requirements.txt
├── Procfile              ← For Railway / Render
└── .env.example          ← Environment variable template
```

---

## 🚀 Quick Start (Local)

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables (or leave defaults for local dev)
cp .env.example .env
# Edit .env as needed

# 4. Run migrations (creates SQLite database)
python manage.py migrate

# 5. Create a Django superuser (for /django-admin/)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver

# Website:       http://localhost:8000/
# Custom admin:  http://localhost:8000/admin/
# Django admin:  http://localhost:8000/django-admin/
# Token (default): hiddenbraj2026
```

---

## 🌐 API Endpoints

### POST `/api/register`
Accepts a registration from the website form.

**Request** (JSON or form-encoded):
```json
{
  "name":      "Ramesh Kumar",
  "phone":     "+91 99999 88888",
  "email":     "ramesh@example.com",
  "city":      "Delhi",
  "tour_type": "weekend",
  "message":   "Family of 4"
}
```

**Response** `201`:
```json
{ "success": true, "message": "Registration successful! We will contact you soon.", "id": 42 }
```

---

### GET `/api/admin-registrations`
Returns all registrations. Requires token.

```
# Via header:
curl -H "Authorization: Bearer BrajDarshan@2026" http://localhost:8000/api/admin-registrations

# Via query param:
curl http://localhost:8000/api/admin-registrations?token=BrajDarshan@2026
```

**Response**:
```json
{
  "stats": { "total": 27, "today": 3, "tours": 18 },
  "registrations": [
    {
      "id": 42,
      "ts": "2026-06-18T10:30:00+05:30",
      "name": "Ramesh Kumar",
      "phone": "+91 99999 88888",
      "email": "ramesh@example.com",
      "city": "Delhi",
      "tourType": "weekend",
      "tourLabel": "Weekend Yatra (Sat–Sun)",
      "message": "Family of 4"
    }
  ]
}
```

---

### GET `/api/admin-export-csv?token=<TOKEN>`
Downloads all registrations as a CSV file (UTF-8 with BOM for Excel).

---

## 🔐 Admin Panel

- **URL:** `http://localhost:8000/admin/`
- **Token:** value of `ADMIN_TOKEN` env var (default: `hiddenbraj2026`)

Features: stats, searchable table, CSV export.

Also available: Django's built-in admin at `/django-admin/` (requires superuser account).

---

## ☁️ Deploy on Railway (Free tier)

1. Push this folder to a GitHub repo
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Set environment variables:
   - `DJANGO_SECRET_KEY` = a long random string
   - `ADMIN_TOKEN` = your secret token
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-app.railway.app`
4. Railway auto-runs `Procfile` → `migrate` + `gunicorn`

---

## ☁️ Deploy on Render (Free tier)

1. Push to GitHub
2. New Web Service → Connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn hiddenbraj.wsgi`
5. Add environment variables (same as Railway)

For a free PostgreSQL DB on Render, add a PostgreSQL service and set `DATABASE_URL`.

---

## 📧 Email Notifications (Optional)

Set these in your `.env`:
```
GMAIL_USER=your@gmail.com
GMAIL_PASS=xxxx-xxxx-xxxx-xxxx   # Gmail App Password (16 chars)
ADMIN_EMAIL=alerts@yourdomain.com
```

To create a Gmail App Password:
→ Google Account → Security → 2-Step Verification → App Passwords

---

## 📊 Google Sheets (Optional)

1. Go to [script.google.com](https://script.google.com) → New project
2. Paste this code:
```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();
  sheet.appendRow([data.id, data.ts, data.name, data.phone,
                   data.email, data.city, data.tourType, data.message]);
  return ContentService.createTextOutput('OK');
}
```
3. Deploy → Web App → "Anyone can access"
4. Set `GOOGLE_SHEET_WEBHOOK=<your web app URL>` in env vars

---

Built with ❤️ for HiddenBraj — Sampurna Braj Yatra
