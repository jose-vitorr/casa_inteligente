from django.db import models

class House(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    owner = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    name = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return f"{self.name} - {self.house.name}"
    
class Device(models.Model):
    name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='devices')
    description = models.TextField(blank=True, null=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} in {self.room.name}"
    
class Scene(models.Model):
    name = models.CharField(max_length=100)
    activated = models.BooleanField(default=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='scenes')

    def __str__(self):
        return self.name

class SceneAction(models.Model):
    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='actions')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='scene_actions')
    interval = models.PositiveIntegerField(default=0)
    order = models.IntegerField()
    newState = models.BooleanField(default=False)

    # Garante que as ações sejam ordenadas pelo campo 'order'
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Action {self.order} - Set to {self.newState} after {self.interval}s"
    
    

