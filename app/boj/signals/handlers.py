from django.db.models.signals import pre_save
from django.dispatch import receiver

from boj import models
from boj import services
from users.models import User


@receiver(pre_save, sender=User)
def auto_wire_boj_user(sender, instance: User, **kwargs):
    assert instance.boj_username
    boj_user, created = models.BOJUser.objects.get_or_create(**{
        models.BOJUser.field_name.USERNAME: instance.boj_username
    })
    if created:
        service = services.get_boj_user_service(instance.username)
        service.update()
