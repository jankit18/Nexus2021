# Generated by Django 3.1.7 on 2021-04-02 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppHome', '0009_auto_20210401_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='timeLast',
            field=models.IntegerField(default=0),
        ),
    ]
