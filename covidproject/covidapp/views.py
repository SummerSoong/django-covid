from http.client import HTTPResponse
from django.shortcuts import render, redirect
import requests
import folium
import geocoder
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from covidproject import local_settings

# /home
def home(request):
	return render(request, 'home.html')

# /statistics
def statistics(request):
	# country list
	country_list = list_countries()
	# map
	map = folium.Map(location=[19,-12], zoom_start=2)
	map = map._repr_html_()
	# if a country is posed, return covid data and map with mark
	if request.method == "POST":
		selected_country = request.POST['selectedcountry']
		if not selected_country == "World":
			map = mark_map(selected_country)
		results = fetch_data(selected_country)
		context = {'details1': results[0], 'details2': results[1], "country_list": country_list, 'map': map, 'country': selected_country}
		return render(request, 'statistics.html', context)
	# else return the covid data of the world and map without mark
	else:
		results = fetch_data("World")
		context = {'details1': results[0], 'details2': results[1], "country_list": country_list, 'map': map, 'country': "World"}
		return render(request, 'statistics.html', context)

# "/contact"
def contact(request):
	# if the request is GET, send an empty form
    if request.method == "GET":
        form = ContactForm()
	# if the request is POST, send the message to a email
    elif request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = f"{form.cleaned_data['message']}\nThis email is from {from_email}"
            try:
                send_mail(subject, message, local_settings.DEFAULT_SENDER, local_settings.EMAIL_LIST)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("/home")
    return render(request, "contact.html", {"form": form})

# redirect "/" to "/home"
def redirect_to_home(request):
	return redirect("/home")

# fetch the countries from covid api and return it by list
def list_countries():
	url = "https://covid-19.dataflowkit.com/v1"
	response = requests.request("GET", url).json()
	# delete the latest update date
	response.pop()
	# delete the first one "World"
	response.pop(0)
	country_list = []
	# save the country text to country_list
	for each_response in response:
		country_list.append(each_response['Country_text'])
	# sort the country_list alphabetically
	sorted_country_list = sorted(country_list)
	# add the "world" to country_list as the first one
	sorted_country_list.insert(0, "World")
	return sorted_country_list

# return "No data" if there is no data from the covid api
def modify_empty_string(string):
	return "No data" if string == "" else string

# fetch the covid data of one country and return it by 2 lists
def fetch_data(country):
	url = f"https://covid-19.dataflowkit.com/v1/{country}"
	response = requests.request("GET", url).json()
	results1 = {
		"Active Cases": modify_empty_string(response['Active Cases_text']),
		"New Cases": modify_empty_string(response['New Cases_text']),
		"New Deaths": modify_empty_string(response['New Deaths_text'])
		}
	results2 = {
		"Total Cases": modify_empty_string(response['Total Cases_text']),
		"Total Deaths": modify_empty_string(response['Total Deaths_text']),
		"Total Recovered": modify_empty_string(response['Total Recovered_text'])
		}
	return [results1, results2]

# return a map with a mark of the location of the country passed
def mark_map(country):
	# get the latitude and longitude of the country
	location = geocoder.osm(country)
	lat = location.lat
	lng = location.lng
	# send the lag and lng to mark it on the map
	map = folium.Map(location=[lat,lng], zoom_start=2)
	folium.Marker([lat, lng], tooltip=f'{country}').add_to(map)
	map = map._repr_html_()
	return map
