# Generated by Django 3.1.2 on 2021-07-23 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20210723_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_new',
            field=models.CharField(blank=True, max_length=65535, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
