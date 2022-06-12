from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User


# Create your models here.
from django.db import connection


class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="media/pics")

    def __str__(self):
        return self.name

class Location(models.Model):
    city = models.ForeignKey(City,on_delete = models.PROTECT)
    pincode  = models.IntegerField()
    name = models.CharField(max_length=50)

    

    def __str__(self):
        return self.name

class Bike_Model(models.Model):
    name= models.CharField(max_length=50)
    location = models.ManyToManyField(Location)
    cost = models.IntegerField()
    image = models.ImageField(upload_to="media/bike_models",blank=True)

    def __str__(self):
        return str(self.name)

    @property
    def available_locations(self):
        return self.location.all()

    @property
    def duration_cost(self):
        return int(self.cost//730)

class Bike(models.Model):
    condition = (
        ('A','Avail'),
        ('B','Booked'),
        ('R','Running'),
        ('U','Unconditioned')
    )
    name = models.CharField(max_length=50)
    model = models.ForeignKey(Bike_Model,on_delete=models.PROTECT)
    location = models.ForeignKey(Location,on_delete= models.PROTECT)
    cost = models.IntegerField()
    status = models.CharField(max_length=50,choices = condition,default='A')
    pick_time = models.DateTimeField(auto_now=False)
    drop_time = models.DateTimeField(auto_now=False)

    @property
    def get_booking_list(self):
        booked = Booked.objects.filter(Q(bike=self.id))
        return booked
    

    def __str__(self):
        return str(self.name)+"-"+str(self.model)+"-" +str(self.id)
# class BikeBooked(models.Model):
#     bike = models.ForeignKey(Bike,on_delete= models.PROTECT)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.PROTECT)
    name=models.CharField(max_length=50)
    pan = models.CharField(max_length=10)
    lincense = models.CharField(max_length=10)
    phone_number = models.IntegerField(null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return str(self.name)

class Booked(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.PROTECT)
    bike = models.ForeignKey(Bike,on_delete=models.PROTECT)
    location = models.ForeignKey(Location,on_delete=models.PROTECT)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False,)
    return_time = models.DateTimeField(auto_now=False, auto_now_add=False,)
    actual_return_time = models.DateTimeField(auto_now=False, auto_now_add=False,)
    ride_cost = models.IntegerField()
    fine_cost = models.IntegerField(default=0)
    total_cost = models.IntegerField()

