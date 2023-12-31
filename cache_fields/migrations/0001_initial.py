# Generated by Django 4.2.7 on 2023-11-05 21:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def add_defaul_statuses(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Status = apps.get_model("cache_fields", "Status")
    Status.objects.bulk_create(
        [
            Status(name="Created"),
            Status(name="InPreparation"),
            Status(name="Shipped"),
            Status(name="Received"),
            Status(name="Delivered"),
        ]
    )

def add_a_package(apps, schema_editor):
    Package = apps.get_model("cache_fields", "Package")
    Package.objects.create(user_id=1,  shipment_cost=1.99, weight=0.05, status_id=1)

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PackageStatusHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('from_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_status', to='cache_fields.status')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cache_fields.package')),
                ('to_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_status', to='cache_fields.status')),
            ],
        ),
        migrations.AddField(
            model_name='package',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cache_fields.status'),
        ),
        migrations.AddField(
            model_name='package',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(code=add_defaul_statuses, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(code=add_a_package, reverse_code=migrations.RunPython.noop),
    ]
