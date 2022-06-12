from django.shortcuts import render
from django.http import request
from django.db.models import Q

import time
from datetime import datetime,date,timedelta
# Create your views here.
from . models import City,Location,Bike_Model,Bike,Booked
from .forms import SearchForm



def index(request):
    cities = City.objects.all()
    return render(request, 'base.html',{'cities':cities})

def rentalSystem(request,pk):
    city_name=City.objects.get(pk=pk).name
    form = SearchForm(request.POST or None)
    cities = City.objects.all()
    locations = Location.objects.filter(city=pk)

    #To extract locations id in a city
    location_ids = []
    for location in locations:
        location_ids.append(location.id)
    
    # print("###################:test_city",test_city)

    
    selected_locations = []
    selected_models = []
    models_in_selected_locations = []
    models_search_by_datetime = []

    # date and time initial values
    pick_date=date.today()
    pick_time=datetime.now().time().replace(second=0, microsecond=0)
    drop_date = pick_date+timedelta(days=30)
    drop_time=pick_time
    # print(pick_date,pick_time,drop_date,drop_time)

    if request.method=="POST":
        pick_date = request.POST.get('pick_date')
        pick_time = request.POST.get('pick_time')
        drop_date = request.POST.get('drop_date')
        drop_time = request.POST.get('drop_time')
        selected_locations += request.POST.getlist('select_location')
        selected_locations = list(map(lambda x: int(x),selected_locations))

        selected_models += request.POST.getlist('selectmodel')
        selected_models = map(lambda x: int(x),selected_models)

    
    pick_date_time = datetime.fromisoformat(str(pick_date)+" "+str(pick_time))
    drop_date_time = datetime.fromisoformat(str(drop_date)+" "+str(drop_time))
    duration = drop_date_time-pick_date_time
    duration = int(duration.total_seconds()//(12*3600))
    print("Duration btwn drop -pick #####",duration)
    booked_bikes = Booked.objects.filter(location__in=location_ids).exclude(Q(start_time__gte=pick_date_time)&
                                        Q(return_time__lte=drop_date_time))
    booked_bike_ids = []
    for i in booked_bikes:
        booked_bike_ids.append(i.bike_id)
    booked_model_ids = [i.model_id for i in  Bike.objects.filter(id__in=booked_bike_ids)]
    print("Booked models ids {} ,Booked bike {}".format(booked_model_ids,booked_bikes))
    selected_models = searchByModel(selected_models)
    models_in_selected_locations += searchByLocation(selected_locations)
    print("#########",location_ids)
    models_in_city = Bike_Model.objects.filter(location__in=location_ids).distinct('id')
    # print(models_in_city)

    filter_model_ids = []
    for model in models_in_selected_locations:
        if model.id not in filter_model_ids:
            filter_model_ids.append(model.id)
    print(filter_model_ids)
    for model in selected_models:
        if model.id not in filter_model_ids:
            filter_model_ids.append(model.id)
    print(filter_model_ids)


    suggested_ids=[]
    for i in location_ids:
        if i not in selected_locations:
            suggested_ids.append(i)
    filter_bike_models = Bike_Model.objects.filter(id__in=filter_model_ids)
    suggested_bike_models = suggestedBikes(suggested_ids,filter_bike_models)
    print("#############",suggested_ids)
    
    print(filter_model_ids)
    
    print(filter_bike_models)
    print(suggested_bike_models)

    location_list = Location.objects.filter(pk__in=location_ids)
    context = {
        'cities': cities,
        'city_name': city_name,
        'form' : form,
        'locations':locations,
        'models_in_city':models_in_city,
        "filter_bike_models":filter_bike_models,
        # "location_list":location_list,
        "suggested_bike_models":suggested_bike_models,
        # "selected_models":selected_models,
        "duration":duration,
        "pick_date":pick_date,
        "pick_time":pick_time,
        "drop_date":drop_date,
        "drop_time":drop_time,
    }
    return render(request, 'bike_rental_app/index.html',context)
    
    

def searchByLocation(selected_locations):
    return Bike_Model.objects.filter(location__in=selected_locations).distinct('name')

def searchByModel(selected_models):
    return Bike_Model.objects.filter(pk__in=selected_models).distinct('name')

def searchByTime():
    pass

def suggestedBikes(suggested_ids,filter_bike_models):
    temp_suggested_bike_models = Bike_Model.objects.filter(location__in=suggested_ids).distinct('name')
    suggested_bike_models = []
    for i in temp_suggested_bike_models:
        if i not in filter_bike_models:
            suggested_bike_models.append(i)
    return suggested_bike_models