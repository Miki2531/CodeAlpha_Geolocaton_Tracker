from django.shortcuts import render
from decouple import config
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
import folium


# Create your views here.
def phone_number(request):
    number  = config('PHONE_NUMBER')
    phonenumber = phonenumbers.parse(number)
    location = geocoder.description_for_number(phonenumber, 'en')
    
    service_provider = phonenumbers.parse(number)
    provider_name = carrier.name_for_number(service_provider, 'en')

    key = config("KEY")
    geocoder_opencage = OpenCageGeocode(key)
    query = str(location)
    results = geocoder_opencage.geocode(query)
    print(results[0]['components']['continent'])
    


    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']
    continent = results[0]['components']['continent']
    timezone = results[0]['annotations']['timezone']['name']
    callingcode = results[0]['annotations']['callingcode']
    

    myMap = folium.Map(location=[lat, lng],  zoom_start=9)
    folium.Marker([lat, lng], popup=location, tooltip='Etho telecome').add_to(myMap)
    myMap.save("location.html")

    context = {
        'continent': continent,
        'location': location,
        'provider_name': provider_name,
        'lat': lat,
        'lng': lng,
        'timezone': timezone,
        'callingcode': callingcode,
    }
    return render(request, 'location.html', context)