import os
import shutil
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def project_image_upload_path(instance, filename):
    # Kreira direktorijum sa nazivom projekta
    if isinstance(instance, Project):
        project_slug = slugify(instance.title)  # Pretvara ime u slug-
        return os.path.join('projects', project_slug, filename)
    elif isinstance(instance, ProjectImage):
        project_slug = slugify(instance.project.title)  # Pretvara ime u slug-
        return os.path.join('projects', project_slug, 'images', filename)

    project_slug = slugify(instance.project.title)  # Pretvara ime u slug-
    return os.path.join('projects', project_slug, 'images', filename)


class Config(models.Model):
    # Naziv parametra (npr. "site_name", "phone_number", "seo_title", itd.)
    name = models.CharField(max_length=255, unique=True)

    # Vrednost parametra (npr. "My Website", "123-456-7890", SEO meta title)
    value = models.TextField()

    # Opcionalan opis koji objašnjava šta ovaj parametar znači
    description = models.TextField(blank=True, null=True)

    # Dodatna vrednost (npr. može biti JSON, URL, dodatna informacija koja nije obavezna)
    additional_value = models.JSONField(default=dict, blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    PROJECT_TYPES = [
        ('furniture', 'Furniture'),
        ('adaptation', 'Adaptation'),
    ]

    title = models.CharField(max_length=255, verbose_name="Naziv projekta")
    short_description = models.CharField(max_length=500, verbose_name="Kratak opis")
    long_description = models.TextField(verbose_name="Dug opis")
    date = models.DateField(null=True, blank=True, verbose_name="Datum")
    main_image = models.ImageField(upload_to=project_image_upload_path, verbose_name="Glavna slika")
    tags = models.ManyToManyField(Tag, related_name="projects")
    slug = models.SlugField(blank=True, null=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='adaptation')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Ako postoji prethodna slika, brišemo je pre čuvanja nove. """

        try:
            if not self.slug:
                self.slug = slugify(self.title)  # Automatski generiše slug iz naslova

            # Pronalaženje prethodne verzije instance
            old_instance = Project.objects.get(pk=self.pk)
            if old_instance.main_image and old_instance.main_image != self.main_image:
                old_path = old_instance.main_image.path
                if os.path.isfile(old_path):
                    os.remove(old_path)  # Brišemo staru sliku sa servera
        except Project.DoesNotExist:
            pass  # Ako objekat ne postoji, to znači da je novi i nema staru sliku

        super().save(*args, **kwargs)  # Čuva novu sliku u bazi


    def delete(self, *args, **kwargs):
        """ Briše glavnu sliku i sve povezane slike pri brisanju projekta """

        # Briše glavnu sliku sa servera
        if self.main_image and os.path.isfile(self.main_image.path):
            os.remove(self.main_image.path)

        # Briše sve slike vezane za projekat
        for image in self.images.all():
            image.delete()  # Ovo će pozvati delete() metodu iz ProjectImage modela

        super().delete(*args, **kwargs)  # Poziva originalnu delete metodu


@receiver(pre_delete, sender=Project)
def delete_project_images(sender, instance, **kwargs):
    """ Briše ceo folder projekta kada se projekat briše """
    if instance.main_image:
        project_folder = os.path.dirname(instance.main_image.path)  # Dobija putanju foldera

        # Proveravamo da li folder postoji i brišemo ga
        if os.path.exists(project_folder):
            shutil.rmtree(project_folder, ignore_errors=True)

    # Brišemo slike vezane za projekat
    for image in instance.images.all():
        image.delete()


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=project_image_upload_path, verbose_name="Sporedna slika")

    def __str__(self):
        return f"Slika za {self.project.title}"

    def delete(self, *args, **kwargs):
        # Provera da li slika postoji na serveru
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)  # Briše sliku sa servera

        super().delete(*args, **kwargs)  # Poziva originalnu delete metodu

    def save(self, *args, **kwargs):
        """ Ako postoji prethodna slika, brišemo je pre čuvanja nove. """

        try:
            # Pronalaženje prethodne verzije instance
            old_instance = ProjectImage.objects.get(pk=self.pk)
            if old_instance.image and old_instance.image != self.image:
                old_path = old_instance.image.path
                if os.path.isfile(old_path):
                    os.remove(old_path)  # Brišemo staru sliku sa servera
        except ProjectImage.DoesNotExist:
            pass  # Ako objekat ne postoji, to znači da je novi i nema staru sliku

        super().save(*args, **kwargs)  # Čuva novu sliku u bazi