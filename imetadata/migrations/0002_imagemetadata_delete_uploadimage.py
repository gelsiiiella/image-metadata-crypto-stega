# Generated by Django 5.0.6 on 2024-11-28 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imetadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='UploadImage',
        ),
    ]
