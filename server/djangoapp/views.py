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


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
# @csrf_exempt
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
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration` view to handle sign up request
# @csrf_exempt
# def registration(request):
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...


# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    context={}
    url = "https://08663624.us-south.apigw.appdomain.cloud/api/review"
    #print(dealer_id)
    # Get dealers from the URL
    dealer_details = get_dealer_reviews_from_cf(url,dealer_id)
    context["dealer_id"]=dealer_id
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        url = "https://08663624.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context = {
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(url)[dealer_id-1].full_name,
            "cars": CarModel.objects.all()
        }
        #print(context)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0#placeholder
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
            print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]=car_parts[0]
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
            json_result = post_request("https://08663624.us-south.apigw.appdomain.cloud/api/review", review, dealerId=dealer_id)
            print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)