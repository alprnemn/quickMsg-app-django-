from django.contrib import admin
from site_app.models import SiteUser,messageDetail,Comments,BannedUsers
# Register your models here.
admin.site.register(SiteUser)
admin.site.register(messageDetail)
admin.site.register(Comments)
admin.site.register(BannedUsers)