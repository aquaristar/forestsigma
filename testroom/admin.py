from django.contrib import admin
from .models import *
# Register your models here.
class ItemChoiceAdmin(admin.ModelAdmin):
	pass
admin.site.register(ItemChoice, ItemChoiceAdmin)

class ItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(Item, ItemAdmin)

class SubscaleAdmin(admin.ModelAdmin):
	pass
admin.site.register(Subscale, SubscaleAdmin)

class TestAdmin(admin.ModelAdmin):
	pass
admin.site.register(Test, TestAdmin)

class TestItemAdmin(admin.ModelAdmin):
	pass
admin.site.register(TestItem, TestItemAdmin)