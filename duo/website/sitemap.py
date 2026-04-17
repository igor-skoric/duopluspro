from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Project


class StaticPageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85
    protocol = "https"

    def items(self):
        return ["home", "about", "projects", "contact"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.65
    protocol = "https"

    def items(self):
        return list(Project.objects.exclude(slug__isnull=True).exclude(slug=""))

    def location(self, obj):
        return reverse("project_details", args=[obj.slug])


sitemaps = {
    "stranice": StaticPageSitemap,
    "projekti": ProjectSitemap,
}
