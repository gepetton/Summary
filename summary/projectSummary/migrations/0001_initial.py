# Generated by Django 4.2.11 on 2024-05-28 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConversionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversion_type', models.CharField(choices=[('OCR', 'OCR'), ('STT', 'STT'), ('GPT', 'GPT')], max_length=3)),
                ('input_data', models.TextField()),
                ('result_data', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]