# django-covid <br />
This web app is to monitor the latest statistics about cases of covid-19 in the world. <br />
Back-end in python django, and front-end should make use of pure javascript. <br />
The covid datat is from API(https://covid-19.dataflowkit.com). <br />
There are three pages: <br />
/home <br />
/statistics <br />
/contact <br />
The home page is static and provide general information about the service. <br />
The statistics page is dynamically generated and contain the following displays: <br />
a. Dropdown from which the user can pick a country or the “world” <br />
b. A map that shows which country is currently selected. <br />
c. A table displaying the different statistics for the world or the selected country.  <br />
The contact page allows the user to send a message to an email address via a contact. <br />
form, in case a user wants to ask for an inquiry. <br />


# building on local environment
    
    # go to covidproject folder
    cd covidproject
    
    # create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # install packages
    pip3 install django django-widget-tweaks requests folium geocoder sendgrid-django
    
    # run server
    python3 manage.py runserver
    
    # open your browser and go to http://127.0.0.1:8000`

# building on Docker
    
    # go to covidproject folder
    cd covidproject
    
    # create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate
    
    # install packages
    pip3 install django django-widget-tweaks requests folium geocoder sendgrid-django
    
    # run server
    python3 manage.py runserver
    
    # open your browser and go to http://127.0.0.1:8000`
