from django.contrib import admin
from .models import Rooms,Topic,Messages,User


admin.site.register(Rooms)
admin.site.register(Topic)
admin.site.register(Messages)
admin.site.register(User)