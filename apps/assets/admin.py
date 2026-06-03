from django.contrib import admin
from .models import AssetType, Asset, AssetField, AssetFieldValue

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_no', 'asset_type', 'customer', 'brand', 'model')
    list_filter = ('asset_type', 'customer__branch')
    search_fields = ('name', 'serial_no', 'customer__name')

@admin.register(AssetField)
class AssetFieldAdmin(admin.ModelAdmin):
    list_display = ('field_name', 'asset_type', 'field_type')
    list_filter = ('asset_type',)

@admin.register(AssetFieldValue)
class AssetFieldValueAdmin(admin.ModelAdmin):
    list_display = ('field', 'asset', 'value')
    search_fields = ('field__field_name',)
