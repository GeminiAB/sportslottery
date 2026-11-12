from ast import Tuple

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

class Game(models.Model): #比賽
    Game_date = models.DateField(verbose_name="比賽日期")
    Away_pointspread = models.FloatField(verbose_name="客讓分")
    Away_win = models.FloatField(verbose_name="客不讓分")
    Away_rest = models.IntegerField(verbose_name="客隊休息天數")
    Away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_games', verbose_name="客隊")
    Away_score = models.IntegerField(verbose_name="客隊得分")
    Home_score = models.IntegerField(verbose_name="主隊得分")
    Home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_games', verbose_name="主隊")
    Home_rest = models.IntegerField(verbose_name="主隊休息天數")
    Home_win = models.FloatField(verbose_name="主不讓分")
    Home_pointspread = models.FloatField(verbose_name="主讓分")
    Game_totals = models.IntegerField(verbose_name="盤口")
    content = models.TextField(verbose_name="比賽備註", blank=True)

    def __str__(self):
        return f"{self.Game_date}"

    # --- 自動計算屬性 ---

    @property
    def total_score(self):
        """總分：客隊得分 + 主隊得分"""
        return self.Home_score + self.Away_score

    @property
    def away_win_status(self):
        """客隊勝負：客隊得分 - 主隊得分 > 0 顯示過，否則不過"""
        return "過" if self.Away_score > self.Home_score else "不過"

    @property
    def home_win_status(self):
        """主隊勝負：主隊得分 - 客隊得分 > 0 顯示過，否則不過"""
        return "過" if self.Home_score > self.Away_score else "不過"

    @property
    def away_pointspread_pass(self):
        """客隊讓分過：客隊得分 - 主隊得分 + 客隊讓分 > 0 顯示過，否則不過"""
        margin = (self.Away_score - self.Home_score) + self.Away_pointspread
        return "過" if margin > 0 else "不過"

    @property
    def home_pointspread_pass(self):
        """主隊讓分過：主隊得分 - 客隊得分 + 主讓分 > 0 顯示過，否則不過"""
        margin = (self.Home_score - self.Away_score) + self.Home_pointspread
        return "過" if margin > 0 else "不過"

    @property
    def over_under_result(self):
        """大小分判定：盤口 > 總分＝小分、盤口 < 總分=大分"""
        if float(self.Game_totals) < float(self.total_score):
            return "大分"
        return "小分"