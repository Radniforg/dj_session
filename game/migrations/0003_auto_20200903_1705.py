# Generated by Django 2.2.10 on 2020-09-03 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20200903_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='games', through='game.PlayerGameInfo', to='game.Player'),
        ),
    ]
