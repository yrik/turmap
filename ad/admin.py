from django.contrib import admin
from ad.models import Ad,Link

class AdAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ad, AdAdmin)

class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Link, LinkAdmin)