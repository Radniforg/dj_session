from django.db import models


class Player(models.Model):
    session_id = models.TextField(null=True)



class Game(models.Model):
    number = models.IntegerField()
    ongoing = models.BooleanField(default=True)
    final_tries = models.IntegerField(null=True)
    players = models.ManyToManyField(
        'Player',
        through='PlayerGameInfo',
        related_name='games'
    )



class PlayerGameInfo(models.Model):
    player = models.ForeignKey(
        'Player',
        verbose_name='Игрок',
        on_delete=models.CASCADE,
    )
    game = models.ForeignKey(
        'Game',
        verbose_name='Игра',
        on_delete=models.CASCADE,
    )
    creator = models.BooleanField(verbose_name='Создатель игры',
                                  default=False)
    announce = models.BooleanField(verbose_name='Активна ли всё еще игра для этого игрока',
                                  default=True)
    tries = models.IntegerField(default=0)
    last_number = models.IntegerField(null=True)

    class Meta:
        unique_together = ('player', 'game')