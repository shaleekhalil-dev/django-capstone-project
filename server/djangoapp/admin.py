from django.contrib import admin
from .models import CarMake, CarModel

# تسجيل الموديلات ليراها الروبوت في لوحة الإدارة
admin.site.register(CarMake)
admin.site.register(CarModel)
