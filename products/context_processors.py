from django.core.cache import cache
from .models import StoreSetting


def store_settings_context(request):
    # دالة get_or_set تقوم بالتالي:
    # 1. تبحث في الذاكرة المؤقتة عن شيء اسمه 'site_settings_cache'
    # 2. إذا لم تجده، تذهب لقاعدة البيانات وتجلبه، ثم تحفظه في الذاكرة لمدة 24 ساعة
    # 3. إذا وجدته، تعيده مباشرة وتتجاهل قاعدة البيانات تماماً!
    
    setting_object = cache.get_or_set(
        'site_settings_cache',          # اسم الورقة الصغيرة (مفتاح الكاش)
        StoreSetting.objects.first(),   # من أين نجلب البيانات لو الورقة فارغة؟
        timeout=60 * 60 * 24            # مدة الاحتفاظ بالورقة بالثواني (هنا 24 ساعة)
    )
    
    return {'site_settings': setting_object}