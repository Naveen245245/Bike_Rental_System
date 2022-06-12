from django.contrib import admin

# Register your models here.
from . models import City,Location,Bike_Model,Bike,Booked,Customer

class CityAdmin(admin.ModelAdmin):
    list_display = ['id','name']
admin.site.register(City,CityAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ['id','name','city','pincode']
admin.site.register(Location,LocationAdmin)

class Bike_ModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','cost']
admin.site.register(Bike_Model,Bike_ModelAdmin)

class BikeAdmin(admin.ModelAdmin):
    list_display = ['id','name','model','location','cost','pick_time','drop_time','status']
admin.site.register(Bike,BikeAdmin)

class BookedAdmin(admin.ModelAdmin):
    list_display = ['id','user','bike','location','start_time','return_time','actual_return_time','total_cost']
admin.site.register(Booked,BookedAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','name','pan','lincense','phone_number','email']
admin.site.register(Customer,CustomerAdmin)