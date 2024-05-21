from django.contrib import admin
from my_app.models import Category, CategoryRegion, Auto, Parking
from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name',)
    list_display_links = ('id', 'category_name',)


@admin.register(CategoryRegion)
class CategoryRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'category',)
    list_display_links = ('id', 'region',)


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'car_name', 'parking_number', 'car_id', 'is_active', 'created_at', 'updated_at', 'category',
        'display_image')
    list_display_links = ('id', 'parking_number',)
    list_filter = ('is_active', 'category',)
    search_fields = ('parking_number', 'car_id',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('parking_number', 'car_name', 'car_id', 'car_qr', 'is_active', 'created_at',)
        }),
        ('Location Information', {
            'fields': ('lat', 'long', 'category',)
        }),
    )

    def display_image(self, obj):
        if obj.car_qr:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px;" />'.format(obj.car_qr.url))
        else:
            return format_html(
                '<img src="{}" style="max-width: 50px; max-height: 50px;" />'.format(
                    '/media/qr/qr/no-photo.png'))

    display_image.short_description = 'Car id rasmi'


class ParkingAdmin(admin.ModelAdmin):
    list_display = ['parking_count', 'is_active']
    list_filter = ['is_active']
    search_fields = ['parking_count']


admin.site.register(Parking, ParkingAdmin)
