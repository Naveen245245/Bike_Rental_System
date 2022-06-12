from django.db.models.signals import post_save
from . models import Bike, Booked
from datetime import datetime

def modify_status(sender, instance, created, **kwargs):
    print("**************** in post signal create bed")
    
    if created == False:
        print(instance.bike)
        bike = Bike.objects.get(pk=instance.bike)
        bike.pick_time = instance.start_time
        bike.drop_time = instance.return_time
        if instance.start_time > datetime.now().time().replace(second=0, microsecond=0):
            bike.status = 'R'
        else:
            bike.status = 'B'
        


post_save.connect(modify_status, sender=Booked)