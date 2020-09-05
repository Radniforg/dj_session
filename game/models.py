from django.db import models


class Player(models.Model):
    cookie = models.CharField(max_length=64,
                              default='nom')

    def __str__(self):
        return self.cookie



class Game(models.Model):
    number = models.IntegerField()
    ongoing = models.BooleanField(default=True)
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
    victor = models.BooleanField(verbose_name='Победитель',
                                 default=False)

    class Meta:
        unique_together = ('player', 'game')