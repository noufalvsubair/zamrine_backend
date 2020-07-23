from django.contrib import admin
from django.contrib.admin import AdminSite
from .model.product import Product, ProductImages, ProductSizes
from .model.review import Reviews
from .model.customer import Customer

class ZamrineAdminSite(AdminSite):
    site_header = "Zamrine Administration"
    site_title = "Zamrine Administration"

admin_site = ZamrineAdminSite()

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'long_name', 'category', 'current_price', 
    'previous_price', 'description', 'soldBy', 'product_type', 'action',)
    ordering = ('short_name',)
    list_display_links = ('action',)
    search_fields= ('short_name', 'long_name')

@admin.register(ProductImages)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'image_url', 'action',)
    list_display_links = ('action',)

    def product_name(self, obj):
           return obj.product.short_name

@admin.register(ProductSizes)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'size', 'action',)
    list_display_links = ('action',)

    def product_name(self, obj):
            return obj.product.short_name

@admin.register(Reviews)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'name', 'title', 'message', 'rating', 'created_at',)

    def product_name(self, obj):
           return obj.product.short_name

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'image_url')

    def name(self, obj):
        return obj.user.get_full_name()

    def email(self, obj):
        return obj.user.email



