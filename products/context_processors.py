from django.core.cache import cache
from .models import StoreSetting


def store_settings_context(request):

    setting_object = cache.get_or_set(
        'site_settings_cache',          
        StoreSetting.objects.first(),   
        timeout=60 * 60 * 24            
    )
    
    return {'site_settings': setting_object}