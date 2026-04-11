import os
import django

# 1. إعداد بيئة جانغو للتعرف على المشروع (اسم مجلد الإعدادات هو LaptopStore)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LaptopStore.settings')
django.setup()

from products.models import Category, Product

def seed_data():
    print("جاري إضافة البيانات، يرجى الانتظار...")
    
    # 2. إنشاء التصنيفات
    categories_data = ['ألعاب (Gaming)', 'برمجة وأعمال', 'تصميم ومونتاج', 'استخدام يومي ودراسة']
    categories = {}
    for cat_name in categories_data:
        cat, created = Category.objects.get_or_create(name=cat_name)
        categories[cat_name] = cat
        
    # 3. بيانات 15 لابتوب
    laptops = [
        {"name": "MacBook Pro M3 Max", "cat": "تصميم ومونتاج", "price": 3499.00, "CPU": "Apple M3 Max", "RAM": "36GB Unified", "storage": "1TB SSD", "GPU": "Apple 30-core GPU", "stock": 10,
         "description": "🌟 **الأداء:** أداء خارق بفضل معالج M3 Max.\n🎯 **الاستخدام المناسب:** المونتاج السينمائي، التصميم ثلاثي الأبعاد، وتطوير البرمجيات المعقدة.\n✨ **المميزات:** شاشة Liquid Retina XDR، بطارية تدوم طويلاً، ونظام تبريد متطور."},
        {"name": "Dell XPS 15", "cat": "برمجة وأعمال", "price": 2299.00, "CPU": "Intel Core i9-13900H", "RAM": "32GB DDR5", "storage": "1TB PCIe SSD", "GPU": "NVIDIA RTX 4070", "stock": 15,
         "description": "🌟 **الأداء:** قوي جداً للمهام المتعددة.\n🎯 **الاستخدام المناسب:** البرمجة المتقدمة، تحليل البيانات، والأعمال الإدارية.\n✨ **المميزات:** شاشة OLED 3.5K حواف نحيفة جداً، تصميم من الكربون فايبر."},
        {"name": "ASUS ROG Strix Scar 17", "cat": "ألعاب (Gaming)", "price": 2899.00, "CPU": "AMD Ryzen 9 7945HX", "RAM": "32GB DDR5", "storage": "2TB SSD", "GPU": "NVIDIA RTX 4080", "stock": 8,
         "description": "🌟 **الأداء:** وحش الألعاب يوفر إطارات عالية جداً.\n🎯 **الاستخدام المناسب:** ألعاب AAA التنافسية، البث المباشر، والـ 3D Rendering.\n✨ **المميزات:** شاشة 240Hz، إضاءة RGB محيطية، تبريد احترافي Liquid Metal."},
        {"name": "Lenovo ThinkPad X1 Carbon", "cat": "برمجة وأعمال", "price": 1799.00, "CPU": "Intel Core i7-1355U", "RAM": "16GB LPDDR5", "storage": "512GB SSD", "GPU": "Intel Iris Xe", "stock": 20,
         "description": "🌟 **الأداء:** ممتاز ومستقر للمهام اليومية.\n🎯 **الاستخدام المناسب:** رواد الأعمال، المبرمجين، والطلاب الجامعيين.\n✨ **المميزات:** كيبورد أسطوري مريح، وزن خفيف جداً، أمان عالي بصمة الوجه والإصبع."},
        {"name": "HP Spectre x360", "cat": "تصميم ومونتاج", "price": 1599.00, "CPU": "Intel Core i7-13700H", "RAM": "16GB DDR4", "storage": "1TB SSD", "GPU": "Intel Iris Xe", "stock": 12,
         "description": "🌟 **الأداء:** سلس وسريع في الاستجابة.\n🎯 **الاستخدام المناسب:** التصميم الجرافيكي 2D، الرسم الرقمي، والعروض التقديمية.\n✨ **المميزات:** شاشة قابلة للطي 360 درجة تدعم اللمس والقلم الذكي، تصميم أنيق."},
        {"name": "Acer Swift 3", "cat": "استخدام يومي ودراسة", "price": 799.00, "CPU": "AMD Ryzen 5 7530U", "RAM": "8GB DDR4", "storage": "512GB SSD", "GPU": "AMD Radeon Graphics", "stock": 30,
         "description": "🌟 **الأداء:** اقتصادي ويفي بالغرض للمهام العادية.\n🎯 **الاستخدام المناسب:** تصفح الإنترنت، تطبيقات الأوفيس، ومشاهدة المحتوى.\n✨ **المميزات:** وزن خفيف، بطارية ممتازة، سعر اقتصادي."},
        {"name": "Razer Blade 16", "cat": "ألعاب (Gaming)", "price": 3299.00, "CPU": "Intel Core i9-13950HX", "RAM": "32GB DDR5", "storage": "1TB SSD", "GPU": "NVIDIA RTX 4090", "stock": 5,
         "description": "🌟 **الأداء:** أقوى أداء جرافيك ممكن في لابتوب.\n🎯 **الاستخدام المناسب:** الألعاب بدقة 4K، تطوير الألعاب، وإنشاء المحتوى.\n✨ **المميزات:** شاشة Mini-LED مزدوجة الدقة، تصميم ألومنيوم فخم."},
        {"name": "Apple MacBook Air M2", "cat": "استخدام يومي ودراسة", "price": 1099.00, "CPU": "Apple M2", "RAM": "8GB Unified", "storage": "256GB SSD", "GPU": "Apple 8-core GPU", "stock": 25,
         "description": "🌟 **الأداء:** سريع جداً وصامت تماماً (بدون مراوح).\n🎯 **الاستخدام المناسب:** الدراسة، البرمجة الخفيفة، والاستخدام اليومي.\n✨ **المميزات:** بطارية خرافية (18 ساعة)، نظام macOS سلس، تصميم نحيف جداً."},
        {"name": "Microsoft Surface Laptop 5", "cat": "برمجة وأعمال", "price": 1299.00, "CPU": "Intel Core i7-1255U", "RAM": "16GB LPDDR5x", "storage": "512GB SSD", "GPU": "Intel Iris Xe", "stock": 18,
         "description": "🌟 **الأداء:** ممتاز لبيئة عمل الويندوز.\n🎯 **الاستخدام المناسب:** الإدارة، كتابة الأكواد، والاستخدام المكتبي.\n✨ **المميزات:** شاشة لمس PixelSense، تصميم ألكانتارا مريح لليد."},
        {"name": "MSI Katana 15", "cat": "ألعاب (Gaming)", "price": 1199.00, "CPU": "Intel Core i7-13620H", "RAM": "16GB DDR5", "storage": "1TB SSD", "GPU": "NVIDIA RTX 4060", "stock": 14,
         "description": "🌟 **الأداء:** أداء ألعاب قوي بسعر متوسط.\n🎯 **الاستخدام المناسب:** ألعاب الـ ESports والمونتاج الخفيف.\n✨ **المميزات:** كيبورد مضيء، معدل تحديث 144Hz، تبريد Cooler Boost."},
        {"name": "LG Gram 17", "cat": "برمجة وأعمال", "price": 1699.00, "CPU": "Intel Core i7-1360P", "RAM": "16GB LPDDR5", "storage": "1TB NVMe SSD", "GPU": "Intel Iris Xe", "stock": 9,
         "description": "🌟 **الأداء:** معالجة سريعة للمهام المكتبية.\n🎯 **الاستخدام المناسب:** البرمجة، الجداول الحسابية الضخمة.\n✨ **المميزات:** شاشة عملاقة 17 بوصة بوزن 1.3 كجم فقط! بطارية تدوم طويلاً."},
        {"name": "Gigabyte AERO 16", "cat": "تصميم ومونتاج", "price": 2399.00, "CPU": "Intel Core i9-13900H", "RAM": "32GB DDR5", "storage": "1TB SSD", "GPU": "NVIDIA RTX 4070", "stock": 7,
         "description": "🌟 **الأداء:** مخصص لصناع المحتوى المحترفين.\n🎯 **الاستخدام المناسب:** تصحيح الألوان، تحرير الفيديو 4K، وتصميم 3D.\n✨ **المميزات:** شاشة 4K OLED معايرة الألوان من المصنع (Pantone)."},
        {"name": "ASUS VivoBook 15", "cat": "استخدام يومي ودراسة", "price": 549.00, "CPU": "Intel Core i3-1215U", "RAM": "8GB DDR4", "storage": "256GB SSD", "GPU": "Intel UHD Graphics", "stock": 40,
         "description": "🌟 **الأداء:** بسيط ومناسب للمهام الأساسية.\n🎯 **الاستخدام المناسب:** الطلاب، كتابة الأبحاث، استهلاك المحتوى.\n✨ **المميزات:** سعر رخيص، تصميم شبابي، لوحة أرقام جانبية."},
        {"name": "Dell Alienware m18", "cat": "ألعاب (Gaming)", "price": 3599.00, "CPU": "Intel Core i9-13980HX", "RAM": "64GB DDR5", "storage": "2TB SSD", "GPU": "NVIDIA RTX 4090", "stock": 4,
         "description": "🌟 **الأداء:** بديل حقيقي للكمبيوتر المكتبي (Desktop Replacement).\n🎯 **الاستخدام المناسب:** أقصى إعدادات للألعاب الحديثة والبرامج الهندسية.\n✨ **المميزات:** شاشة ضخمة 18 بوصة، كيبورد ميكانيكي (Cherry MX)."},
        {"name": "Lenovo Legion Pro 5i", "cat": "ألعاب (Gaming)", "price": 1499.00, "CPU": "Intel Core i7-13700HX", "RAM": "16GB DDR5", "storage": "1TB SSD", "GPU": "NVIDIA RTX 4070", "stock": 11,
         "description": "🌟 **الأداء:** توازن مثالي بين السعر والأداء.\n🎯 **الاستخدام المناسب:** الألعاب القوية، التصميم الهندسي.\n✨ **المميزات:** شاشة WQXGA 165Hz، نظام تبريد Legion Coldfront 5.0."}
    ]

    # 4. إدخال اللابتوبات في قاعدة البيانات
    count = 0
    for data in laptops:
        cat = categories[data["cat"]]
        # نستخدم get_or_create لتجنب التكرار إذا قمت بتشغيل الملف أكثر من مرة
        product, created = Product.objects.get_or_create(
            name=data["name"],
            defaults={
                'category': cat,
                'price': data["price"],
                'CPU': data["CPU"],
                'RAM': data["RAM"],
                'storage': data["storage"],
                'GPU': data["GPU"],
                'stock': data["stock"],
                'description': data["description"]
            }
        )
        if created:
            count += 1

    print(f"✅ تم تنفيذ السكريبت بنجاح! تمت إضافة {count} لابتوب جديد.")

if __name__ == '__main__':
    seed_data()