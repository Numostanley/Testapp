from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(DataTransactions)
admin.site.register(Wallet)
admin.site.register(DataBundle)
