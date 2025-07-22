from django.db import models
from .utils import offer_upload_path


# Create your models here.
class Project(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planirano'),
        ('active', 'Aktivno'),
        ('paused', 'Pauzirano'),
        ('completed', 'Završeno'),
        ('cancelled', 'Otkazano'),
    ]

    name = models.CharField(max_length=255)
    client = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    cost = models.IntegerField(default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.client} "


class Advance(models.Model):
    METHOD_CHOICES = [
        ('kes', 'Keš'),
        ('racun', 'Račun'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='advances')
    amount = models.IntegerField()
    date = models.DateField()
    note = models.TextField(blank=True)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='kes')

    def __str__(self):
        return f"{self.project} - {self.amount} {self.get_method_display()}"


class Contact(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contacts')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.project.name})"


class Offer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='offers')
    file = models.FileField(upload_to=offer_upload_path, null=True, blank=True)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ponuda za {self.project.name} ({self.file.name})'


class Material(models.Model):
    UNIT_CHOICES = [
        ('kom', 'Komad'),
        ('kg', 'Kilogram'),
        ('m', 'Metar'),
        ('m2', 'Metar kvadratni'),
        ('m3', 'Metar kubni'),
        ('l', 'Litar'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='materials')
    type = models.ForeignKey('MaterialType', on_delete=models.CASCADE)  # izaberi tip materijal
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE)  # izaberi tip materijal
    price = models.IntegerField()
    note = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.type.name} - {self.quantity} {self.unit}"


class Worker(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='workers')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    cost = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.position}"


class MaterialType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name