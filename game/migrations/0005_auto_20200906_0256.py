# Generated by Django 2.2.10 on 2020-09-05 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20200906_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playergameinfo',
            name='announce',
            field=models.BooleanField(default=False, verbose_name='Активна ли всё еще игра для этого игрока'),
        ),
    ]
