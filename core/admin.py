from django.contrib import admin
from django.contrib.sessions.models import Session 

# Register your models here.
from .models import (
    Customer,
    ClotheProduct,
    Image,
    Category,
    Order,
    OrderProduct,
    CosmeticProduct,
    AccessorieProduct,
    BillingInfo

)

class ImageAdmin(admin.StackedInline):
    model = Image


@admin.register(ClotheProduct)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageAdmin
    ]

    class Meta:
        model = ClotheProduct


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     pass 



admin.site.register(Customer)
admin.site.register(Session)
admin.site.register(Category)
admin.site.register(OrderProduct)
admin.site.register(Order)
admin.site.register(CosmeticProduct)
admin.site.register(AccessorieProduct)
admin.site.register(BillingInfo)  




