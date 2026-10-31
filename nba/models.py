from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Team(models.Model): #城市 球隊 分區 戰績 勝率
    CONFERENCE_CHOICES = [
        ('EAST', '東區'),
        ('WEST', '西區'),
    ]

    city = models.CharField(max_length=50, verbose_name="城市名稱")
    name = models.CharField(max_length=10, verbose_name="球隊名稱")
    conference = models.CharField(max_length=10, choices=CONFERENCE_CHOICES, verbose_name="分區")
    wins = models.PositiveIntegerField(default=0, verbose_name="勝場")
    losses = models.PositiveIntegerField(default=0, verbose_name="負場")

    class Meta:
        verbose_name = "球隊"

    def __str__(self):
        return f"{self.city} {self.name}"

    @property
    def win_rate(self) -> float:
        """勝率動態計算"""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return round(self.wins / total_games, 1)

