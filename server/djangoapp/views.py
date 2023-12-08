import re
from venv import create
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
import logging
import json
from .restapis import get_dealers_from_cf, post_request, get_dealer_reviews_from_cf
from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            error_message = 'Invalid login, please try again'
            return HttpResponse(status=401, content=error_message)
    
    return render(request, 'djangoapp/index.html')


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return render(request, 'djangoapp/index.html')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
    
        if not User.objects.filter(username=username).exists():
            user = User.objects.create(username=username, first_name=firstname, last_name=lastname, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html')
        else:
            error_message = 'Username already taken'
        return render(request, 'djangoapp/registration.html', {'error_message' : error_message})
    
    return render(request, 'djangoapp/registration.html')
    

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "/api/dealership"
        # Get dealers from the URL
        context = {'dealerships' : get_dealers_from_cf(url)}

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = 'https://ydenbusiness-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get'
        context = {'reviews' : get_dealer_reviews_from_cf(url, dealer_id)}

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    if request.method == "GET":
        dealersid = dealer_id
        url = "https://5b93346d.us-south.apigw.appdomain.cloud/dealerships/dealer-get?dealerId={0}".format(dealersid)
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": "{request.user.first_name} {request.user.last_name}",
                "dealership": dealer_id,
                "review": form["content"],
                "purchase": form.get("purchasecheck"),
                }
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"]= car.year.strftime("%Y")
            json_payload = {"review": review}
            print (json_payload)
            url = "https://5b93346d.us-south.apigw.appdomain.cloud/dealerships/reviews/review-post"
            post_request(url, json_payload, dealerId=dealer_id)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("/djangoapp/login")

