# Generated by Django 3.0 on 2021-06-02 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210602_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
