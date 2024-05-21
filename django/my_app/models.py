from django.db import models
import qrcode
from io import BytesIO
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Kategoriyalar"
        verbose_name_plural = "Kategoriya"


class CategoryRegion(models.Model):
    region = models.CharField(max_length=25, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    car_count = models.IntegerField(default=0)

    def __str__(self):
        return self.region

    def increment_car_count(self):
        if self.category is not None:
            self.car_count += 1
            self.save()

    class Meta:
        verbose_name = "Regionlar"
        verbose_name_plural = "Region"


class Parking(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    parking_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_active = models.BooleanField(default=False)
    cars_foreign = models.ForeignKey('Auto', on_delete=models.CASCADE, blank=True, null=True, related_name='parking')

    def __str__(self):
        return str(self.parking_count)

    class Meta:
        verbose_name = "Parking"
        verbose_name_plural = "Parking"


class Auto(models.Model):
    car_name = models.CharField(max_length=25, blank=True, null=True)
    car_id = models.CharField(max_length=25, blank=True, null=True)
    car_qr = models.ImageField(upload_to='qr/', blank=True, null=True)
    is_active = models.BooleanField()
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CategoryRegion, on_delete=models.CASCADE, blank=True, null=True)
    parking_number = models.ForeignKey(Parking, on_delete=models.CASCADE, blank=True, null=True, related_name='autos')

    def __str__(self):
        return str(self.parking_number)

    def save(self, *args, **kwargs):
        if self.category is not None and self.category.car_count is not None:
            if self.category.car_count >= 100:
                raise ValidationError("Boshqa mashina qoshish mumkin emas")

        super().save(*args, **kwargs)

        if self.category is not None:
            self.category.increment_car_count()

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


@receiver(post_save, sender=Auto)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:
        qr_data = f"Parking Number: {instance.parking_number}\nCar name: {instance.car_name}\nCar ID: {instance.car_id}\nLatitude: {instance.lat}\nLongitude: {instance.long}\nIs Active: {instance.is_active}\nCreated At: {instance.created_at}"
        qr = qrcode.make(qr_data)
        if qr.mode != 'RGB':
            qr = qr.convert('RGB')
        qr_bytes = BytesIO()
        qr.save(qr_bytes, format='PNG')

        instance.car_qr.save(f'qr/{instance.car_id}.png', ContentFile(qr_bytes.getvalue()), save=False)
        instance.save()
