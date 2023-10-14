from django.contrib import admin
from api.models import User, IdentityCards, PassportDetails

# Register your models here.
admin.site.register(User)
admin.site.register(IdentityCards)
admin.site.register(PassportDetails)