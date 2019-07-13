from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Product)
admin.site.register(models.Entry)


class EntryInline(admin.StackedInline):
    model = models.Entry
    extra = 2

class OrderAdmin(admin.ModelAdmin):
    fields = 'customer', 'address'
    inlines = EntryInline,

admin.site.register(models.Order, OrderAdmin)

