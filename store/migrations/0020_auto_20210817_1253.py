# Generated by Django 3.1.2 on 2021-08-17 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20210805_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=65535, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='combo',
            field=models.CharField(max_length=65535, null=True),
        ),
    ]