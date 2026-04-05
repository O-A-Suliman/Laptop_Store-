from .models import StoreSetting
def store_settings_context(request):
    setting_object=StoreSetting.objects.first()
    return {'site_settings': setting_object}