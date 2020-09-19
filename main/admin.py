from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import donate_model, transaction_model
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class donate_model_Admin(ImportExportModelAdmin):
    list_display = ('name','phone','email','amount',)

class transaction_model_Admin(ImportExportModelAdmin):
    list_display = ('made_by', 'made_on', 'amount', 'order_id', 'checksum',)

admin.site.site_header = 'DONATIONS'
admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(donate_model, donate_model_Admin)
admin.site.register(transaction_model, transaction_model_Admin)