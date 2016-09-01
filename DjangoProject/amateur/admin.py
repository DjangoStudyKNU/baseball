from django.contrib import admin
from amateur.models import *
# Register your models here.



admin.site.register(AmateurTeam)
admin.site.register(AmateurLeague)
admin.site.register(AmateurGamePlace)
admin.site.register(Region)
admin.site.register(AmateurGameSchedule)
admin.site.register(AmateurTeamHasLeague)
admin.site.register(AmateurPitcherHasTeam)
admin.site.register(AmateurHitterHasTeam)
admin.site.register(AmateurPitcherHasLeague)
admin.site.register(AmateurHitterHasLeague)
admin.site.register(AmateurGameDetailHitter)
admin.site.register(AmateurGameDetailPitcher)




