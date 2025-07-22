

def offer_upload_path(instance, filename):
    # Fajl će biti snimljen u folder "offers/project_<id>/filename"
    return f'offers/project_{instance.project.id}/{filename}'