from django.contrib import admin
from .models import Config, Project, ProjectImage, Tag

# Register your models here.

admin.site.register(Config)
# admin.site.register(ProjectImage)
admin.site.register(Tag)


# Inline model za ProjectImage
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Podesite broj praznih obrazaca za slike koje želite da budu prikazane
    verbose_name = 'Slika'
    verbose_name_plural = 'Slike'


# Admin za Project model
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ['title', 'date']
    search_fields = ['title', 'tags__name']  # Omogućava pretragu po nazivu i tagovima


admin.site.register(Project, ProjectAdmin)