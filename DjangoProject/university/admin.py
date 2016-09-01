from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from university.models import *
# from university.forms import CustomUserChangeForm, CustomUserCreationForm


admin.site.register(UniversityTeam)
admin.site.register(UniversityLeague)
admin.site.register(UniversityGamePlace)
admin.site.register(Player)
admin.site.register(University)
admin.site.register(UniversityGameSchedule)
admin.site.register(UniversityTeamHasLeague)
admin.site.register(UniversityPitcherHasTeam)
admin.site.register(UniversityHitterHasTeam)
admin.site.register(UniversityPitcherHasLeague)
admin.site.register(UniversityHitterHasLeague)
admin.site.register(UniversityGameDetailHitter)
admin.site.register(UniversityGameDetailPitcher)




