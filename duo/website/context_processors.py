from .models import Config, Project
from django.db.models.functions import Random


def site_config(request):
    # Povući sve podatke iz Config modela i vratiti ih u kontekstu

    adaptation = Project.objects.filter(project_type='adaptation').order_by(Random())[:3]
    furniture = Project.objects.filter(project_type='furniture').order_by(Random())[:3]

    config_data = {config.name: config for config in Config.objects.all()}
    return {'site_config': config_data, 'adaptation': adaptation, 'furniture': furniture}
