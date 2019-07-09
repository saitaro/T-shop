# Generated by Django 2.2 on 2019-07-05 00:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20190705_0043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'entries'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='entries',
        ),
        migrations.AlterField(
            model_name='entry',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='store.Order'),
        ),
    ]
