# Generated by Django 3.2.6 on 2021-12-27 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20211227_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=16, unique=True, verbose_name='유저 이름'),
        ),
    ]