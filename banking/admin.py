from django.contrib import admin
from .models import Client, CompteBancaire, Operation

admin.site.register(Client)
admin.site.register(CompteBancaire)
admin.site.register(Operation)