from .models import Config, Project
from django.db.models.functions import Random

SEO_DEFAULT_DESCRIPTION = (
    "DuoPlusPro — izrada nameštaja po meri (kuhinje, plakari, komode) i kompletna adaptacija stanova: "
    "građevinski radovi, elektrika, voda, podovi, pločice i završna obrada enterijera."
)


def site_config(request):
    adaptation = Project.objects.filter(project_type="adaptation").order_by(Random())[:3]
    furniture = Project.objects.filter(project_type="furniture").order_by(Random())[:3]

    config_data = {config.name: config for config in Config.objects.all()}

    scheme = "https" if request.is_secure() else request.scheme
    host = request.get_host()
    site_origin = f"{scheme}://{host}".rstrip("/")
    canonical_url = request.build_absolute_uri(request.path)

    return {
        "site_config": config_data,
        "adaptation": adaptation,
        "furniture": furniture,
        "site_origin": site_origin,
        "canonical_url": canonical_url,
        "seo_default_description": SEO_DEFAULT_DESCRIPTION,
    }

