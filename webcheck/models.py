from django.db import models
import uuid
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
import os
from django.conf import settings


class UrlCheck(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'


class Test(models.Model):
    TEST_STATUS_OPTIONS = [
        ('IN-PROGRESS', 'IN-PROGRESS'),
        ('COMPLETED', 'COMPLETED'),
        ('QUEUED', 'QUEUED'),
        ('FAILED', 'FAILED'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test_type = models.CharField(max_length=50)
    url_check = models.ForeignKey(UrlCheck, on_delete=models.CASCADE, related_name='tests')
    status = models.CharField(max_length=25, choices=TEST_STATUS_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
    result = models.BooleanField(null=True)
    details = models.TextField(null=True)
    proof_image = models.BooleanField(default=False)


@receiver(post_save, sender=UrlCheck)
def after_url_check_create(sender, instance, created, **kwargs):
    if created:
        from .tasks import create_tests
        create_tests.delay(instance.id)
        pass


@receiver(pre_delete, sender=Test)
def before_test_delete(sender, instance, **kwargs):
    if instance.proof_image:
        media_root = settings.MEDIA_ROOT
        file_name = f'{instance.id}.png'
        file_path = os.path.join(media_root, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
    pass
