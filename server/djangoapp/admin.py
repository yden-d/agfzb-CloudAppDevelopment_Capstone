from django.contrib import admin
from .models import CarMake, CarModel
# from .models import related models


# Register your models here.
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 2
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['make', 'name', 'dealer_id', 'type', 'year']
    list_filter = ['make', 'type', 'year']
    search_fields = ['make', 'name']
    
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)