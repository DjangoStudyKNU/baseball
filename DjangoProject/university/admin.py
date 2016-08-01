from django.contrib import admin
from university.models import *

admin.site.register(Team)
admin.site.register(League)
admin.site.register(GamePlace)
admin.site.register(Player)
admin.site.register(University)
admin.site.register(GameSchedule)
admin.site.register(TeamHasLeague)
admin.site.register(PitcherHasTeam)
admin.site.register(HitterHasTeam)
admin.site.register(PitcherHasLeague)
admin.site.register(HitterHasLeague)
admin.site.register(GameDetailHitter)
admin.site.register(GameDetailPitcher)




