from django.contrib import admin
from .models import House, Room, Device, Scene, SceneAction

# Register your models here.
admin.site.register(House)
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(Scene)
admin.site.register(SceneAction)