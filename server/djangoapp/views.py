# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from restapis import get_request, analyze_review_sentiments


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    '''
    check if get or post
    if get, return registration page
    if post, retrieve registration post details

        if username already exists:
            retrieve user and log them in?
        else
        if specified username does not exist, create user
        if error creating user
        catch exception
            return message error creating user
        
        return render home page with context of user logged in

    '''
    data = json.loads(request.body)
    username=data['userName']
    firstname=data['firstName']
    lastname=data['lastName']
    email = data['email']
    password = data['password']
    user_exist = False

    try:

        User.objects.get(username=username)
        user_exist=True
        #already exists
    except:
        logger.debug("{} is a new User".format(username))
    
    if not user_exist:
        user = User.objects.create_user(username=username,email=email,password=password,first_name=firstname,last_name=lastname)
        login(request,user)
        data={'userName': username, "status":"Authenticated"}
        return JsonResponse(data)
    else:
        data = {'userName': username, "error": "Already Registered"}
        return JsonResponse(data)


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
#Update the `get_dealerships` render list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})


# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request,dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+dealer_id
        data = get_request(endpoint)
        reviews = json.loads(data)
        for rev in reviews:
            sentiment = analyze_review_sentiments(rev['review'])
            rev['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    #endpoing/dealer_id
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealer_details = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer_details})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
