from django.contrib import admin
from .models import (
    Profile,
    Activity,
    ActivityPoint,
    Comment,
    Kudos,
    Follower,
    UserMonthlyStats
)

# This makes all your tables show up in the admin panel
admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(ActivityPoint)
admin.site.register(Comment)
admin.site.register(Kudos)
admin.site.register(Follower)
admin.site.register(UserMonthlyStats)

