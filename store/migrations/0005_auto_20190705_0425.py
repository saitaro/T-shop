# Generated by Django 2.2 on 2019-07-05 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20190705_0306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='store.Order'),
        ),
    ]
