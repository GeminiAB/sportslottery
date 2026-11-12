from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Team, Game

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'conference', 'wins', 'losses', 'win_rate_display')
    list_filter = ('conference',)
    search_fields = ('name',)

    def win_rate_display(self, obj): #將 Model 中的勝率屬性顯示在後台列表
        return obj.win_rate
    win_rate_display.short_description = '勝率%'

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('Game_date', 'Away_pointspread', 'Away_win', 'Away_team')
