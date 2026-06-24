from django.conf import settings

def google_maps(request):
    """Make GOOGLE_MAPS_API_KEY available in all templates."""
    return {
        'GOOGLE_MAPS_API_KEY': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
