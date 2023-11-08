from typing import Any

from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

UserModel = get_user_model()

class Status(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self) -> str:
        return self.name


class Package(DirtyFieldsMixin, models.Model):  # Solution 4
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    shipment_cost = models.DecimalField(max_digits=6, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.cached_status_id = self.status_id  # Solution 3

    def __str__(self) -> str:
        return f"{self.id}: {self.status}"


class PackageStatusHistory(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    from_status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='from_status', null=True)
    to_status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='to_status')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.package_id}: {self.from_status_id} -> {self.to_status_id}"

@receiver(post_save, sender=Package)
def register_status_change(sender, instance: Package, **kwargs):
    # old_status_id = instance.id and Package.objects.get(id=instance.id).status_id  # Solution 2
    # old_status_id = instance.cached_status_id  # Solution 3
    old_status_id = instance.get_dirty_fields(check_relationship=True).get("status", None)  # Solution 4

    if instance.status_id != old_status_id:
        # There is a status change
        PackageStatusHistory.objects.create(package_id=instance.id,
                                            from_status_id=old_status_id,
                                            to_status_id=instance.status_id)
