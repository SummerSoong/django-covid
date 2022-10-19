from http.client import HTTPResponse
from django.shortcuts import render, redirect
import requests
import folium
import geocoder
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import ContactForm
from covidproject import local_settings

def home(request):
	return render(request, 'home.html')

def statistics(request):
	country_list = list_countries()
	map = folium.Map(location=[19,-12], zoom_start=2)
	map = map._repr_html_()
	if request.method == "POST":
		selected_country = request.POST['selectedcountry']
		if not selected_country == "World":
			map = mark_map(selected_country)
		results = fetch_data(selected_country)
		context = {'details1': results[0], 'details2': results[1], "country_list": country_list, 'map': map, 'country': selected_country}
		return render(request, 'statistics.html', context)
	else:
		results = fetch_data("World")
		context = {'details1': results[0], 'details2': results[1], "country_list": country_list, 'map': map, 'country': "World"}
		return render(request, 'statistics.html', context)


def contact(request):
    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = f"{form.cleaned_data['message']} from {from_email}"
            try:
                send_mail(subject, message, local_settings.DEFAULT_SENDER, local_settings.EMAIL_LIST)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("/home")
    return render(request, "contact.html", {"form": form})

def redirect_to_home(request):
	return redirect("/home")

def list_countries():
	url = "https://covid-19.dataflowkit.com/v1"
	response = requests.request("GET", url).json()
	response.pop()
	response.pop(0)
	country_list = []
	for each_response in response:
		country_list.append(each_response['Country_text'])
	sorted_country_list = sorted(country_list)
	sorted_country_list.insert(0, "World")
	return sorted_country_list

def modify_empty_string(string):
	return "No data" if string == "" else string

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

def mark_map(country):
	location = geocoder.osm(country)
	lat = location.lat
	lng = location.lng
	map = folium.Map(location=[lat,lng], zoom_start=2)
	folium.Marker([lat, lng], tooltip=f'{country}').add_to(map)
	map = map._repr_html_()
	return map
