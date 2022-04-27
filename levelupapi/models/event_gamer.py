from django.db import models

class Event_gamer(models.Model):
    gamer = models.ForeignKey("gamer", on_delete=models.CASCADE )
    event = models.ForeignKey("event", on_delete=models.CASCADE )