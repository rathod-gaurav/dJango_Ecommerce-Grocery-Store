# Generated by Django 4.0.5 on 2022-06-12 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_colorvariant_quantityvariant_sizevariant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='catrgory',
            new_name='category',
        ),
    ]
