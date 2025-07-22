from django.contrib import admin
from .models import Project, Advance, Contact, Offer, Material, MaterialType, Unit, Worker

admin.site.register(Project)
# admin.site.register(Advance)
# admin.site.register(Contact)
admin.site.register(Material)
admin.site.register(MaterialType)
admin.site.register(Unit)
admin.site.register(Worker)


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('project', 'file', 'uploaded_at')
    search_fields = ('description',)
    list_filter = ('uploaded_at',)