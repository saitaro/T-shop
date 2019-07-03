# Generated by Django 2.2.2 on 2019-06-15 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190615_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uploader',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]
