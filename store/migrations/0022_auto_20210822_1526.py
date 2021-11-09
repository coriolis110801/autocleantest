# Generated by Django 3.1.2 on 2021-08-22 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20210822_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.CharField(max_length=65535, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='combo',
            field=models.CharField(max_length=65535, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]