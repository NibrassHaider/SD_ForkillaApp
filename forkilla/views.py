import datetime

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.

from django.urls import reverse

from forkilla.forms import ReservationForm, ReviewForm, CommercialForm, LoginForm
from .models import Restaurant, ViewedRestaurants, Review, Profile, Reservation
import random

from django.contrib.auth.models import Group
from rest_framework import viewsets
from .serializers import RestaurantSerializer

def home(request):
    #all_restaurants(request)
    com = User.objects.all()
    print(com, "aquiiiiii")
    if(request.method=="POST"):
        print("hello")
        #form =  UserCreationForm(request.POST)
        form = CommercialForm(request.POST)
        print(form.fields)
        print(form.errors)
        if(form.errors):
            print(form.errors)
            errors = form.errors
            form = CommercialForm()
            error = True
            context = {'form': form , 'errors' : error,'message':errors}
            #return render(request,'forkilla/home.html',context)
            return render(request,'forkilla/home_signup.html',context)

        if(form.is_valid()and not form.errors):
            print("aquiiiiii")
            user = form.save()
            print(user.password)
            pass1 = form.cleaned_data['password1']
            user.set_password(pass1)
            user.save()

            com = Profile.objects.all()
            print(com, "aquiiiiii")
        return HttpResponseRedirect(reverse('index'))
    else:
        form = CommercialForm()
        context = {'form':form}
        #return render(request,'forkilla/home.html',context)
        return render(request,'forkilla/home_signup.html',context)

def login(request):
    if request.method == 'POST':
        msg = False
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(password)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            form = LoginForm()
            msg = True
            print(msg)
            return render(request, 'forkilla/login.html', {'form': form,'msg':msg,'message':"Invalid Login details given"})
    else:
        form = LoginForm()
        return render(request, 'forkilla/login.html', {'form':form})

@login_required(login_url='login')
def index(request):
     print(request.user.id,"iDDDDDD")
     #return HttpResponse("Hello, world. You're at the Forkilla home page.");
     promoted_restaurants = Restaurant.objects.filter(is_promot="True")
     viewedrestaurants = _check_session(request)
     print(viewedrestaurants.restaurant.all())
     print(promoted_restaurants)
     oontext = { "promoted_restaurants" :promoted_restaurants
                 , 'viewed_restaurants': viewedrestaurants
            }
     return render(request,'forkilla/base.html', oontext)

def restaurants(request, city="",category=""):

    filter_by_category = False
    promoted = False
    cc = False
    city_c = False
    menu = False
    print(category)
    rest = request.GET.get('rest')
    print(rest)
    if request.method == "GET":
        if(request.GET.get('rest')):
            #print("gggg")
            restaurants_by_city = Restaurant.objects.filter(city=request.GET.get('rest'))
            city_c = True
            context = {
                'city': city_c,
                'restaurants': restaurants_by_city,
            }
            return render(request, 'forkilla/restaurants.html', context)

    if(city.find("/")):
        splitted = city.split('/')

    if (len(splitted)==2 and category):
        category = category.replace('-',' ')
        restaurants_by_city = Restaurant.objects.filter(city__iexact=splitted[0], category=splitted[1],
        menu_description=category)
        menu = True;

    elif(city and category):
        restaurants_by_city = Restaurant.objects.filter(city__iexact=city ,category=category)
        cc = True
    elif city:
        restaurants_by_city = Restaurant.objects.filter(city__iexact=city)
        city_c = True
    elif category:
        restaurants_by_city = Restaurant.objects.filter(category=category)
        filter_by_category = True

    else:
        restaurants_by_city = Restaurant.objects.filter(is_promot="True")
        promoted = True

    context = {
        'cc' : cc,
        'filter_category' : filter_by_category ,
        'city': city_c,
        'restaurants': restaurants_by_city,
        'promoted': promoted,
        'menu':menu

    }
    return render(request, 'forkilla/restaurants.html', context)

def all_restaurants(request):
    restaurants = []
    diccionari = {"barcelona":"spain","paris":"france","berlin":"germany","londres":"england",
                  "roma":"italy","atenas":"greece","hong kong":"china"}

    for i in range(1,13):
        id_exists = Restaurant.objects.filter(restaurant_number= i).exists()
        if(id_exists):
            continue
        category = Restaurant. _d_categories

        comida, origen = random.choice(list(category.items()))
        ciudad, pais = random.choice(list(diccionari.items()))
        print(ciudad,pais,comida,origen)
        #restaurant = Restaurant(category=comida,city=ciudad,country=pais)
        restaurant = Restaurant.objects.create(restaurant_number=str(i), name='',menu_description="Only Tapas",price_average=0,
            is_promot=True,
            rate=0,
            address="",
            city=ciudad,country=pais,featured_photo =None,category=comida,capacity=10
                                               )
        print("City: ",restaurant.category)
        restaurant.save()
        restaurants.append(restaurant)
        print(restaurants)

    context = {
        'restaurants':Restaurant.objects.all()
    }
    return render(request, 'forkilla/all_restaurants.html', context)


def details(request,restaurant_number=""):
    viewed_restaurants = _check_session(request)
    restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
    print(restaurant,"reeee")
    viewed_restaurants.restaurant.add(restaurant)
    restaurant1 = Review.objects.filter(number = restaurant.restaurant_number)
    for i in restaurant1:
        print(i.message , ".....................")
    #restaurant1 = Review.objects.filter(user=request.user).all()
    context = {
        'details': restaurant,
        'viewed_restaurants': viewed_restaurants,
        'msg':restaurant1
    }
    return render(request, 'forkilla/details.html', context)

@login_required(login_url='login')
def reservation(request):
    try:
        if request.method == "POST":
            form = ReservationForm(request.POST)
            form1 = form
            if form.is_valid():
                    resv = form.save(commit=False)
                    restaurant_number = request.session["reserved_restaurant"]

                    resv.restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
                    print(form.cleaned_data['num_people']," : Capacity : ", resv.restaurant.capacity)

                    if( resv.restaurant.capacity - form.cleaned_data['num_people'] < 0 or resv.restaurant.capacity < form.cleaned_data['num_people']):
                        restaurants_by_city = Restaurant.objects.filter(is_promot="True")
                        promoted = True
                        context = {
                            'alert': " Error , Not have much space , try to enter a less number of people " ,
                            'restaurants': restaurants_by_city,
                            'promoted': promoted
                        }
                        return render(request, 'forkilla/restaurants.html', context)
                    else :
                        resv.restaurant.capacity = resv.restaurant.capacity - form.cleaned_data['num_people']
                        print("Capacity after reserving : ", resv.restaurant.capacity)
                        resv.save()
                        request.session["reservation"] = resv.id
                        request.session["result"] = "OK"
                        #resv.user = request.user.id
                    resv.restaurant.save()
                    resv.save()

                    request.session["reservation"] = resv.id
                    request.session["result"] = "OK"
                    return HttpResponseRedirect(reverse('restaurants'))

            else:
                  request.session["result"] = form.errors
            return HttpResponseRedirect(reverse('checkout'))

        elif request.method == "GET":
            restaurant_number = request.GET["reservation"]
            restaurant = Restaurant.objects.get(restaurant_number=restaurant_number)
            request.session["reserved_restaurant"] = restaurant_number

            form = ReservationForm()
            form.initial['user'] = request.user
            context = {
                'restaurant': restaurant,

                'form': form
            }
    except Restaurant.DoesNotExist:
        return HttpResponse("Restaurant Does not exists")
    return render(request, 'forkilla/reservation.html', context)

def checkout(request):
    context = {
        'checkout':"Ready"
    }
    return render(request,'forkilla/checkout.html',context)

def _check_session(request):

    if "viewedrestaurants" not in request.session:
        viewedrestaurants = ViewedRestaurants()
        viewedrestaurants.save()
        request.session["viewedrestaurants"] = viewedrestaurants.id_vr
    else:
        viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])
    return viewedrestaurants

@login_required(login_url='login')
def review(request,restaurant_number=""):
    r = restaurant_number
    if(request.method=="POST"):
        form = ReviewForm(request.POST)
        error = False
        if(form.is_valid()):
            rev = form.save(commit=False)
            number = form.cleaned_data['number']
            rev.restaurant = Restaurant.objects.get(restaurant_number=number)
            print(rev.restaurant,": restaurant")

            message = form.cleaned_data['message']
            rating = form.cleaned_data['rating']
            if(rating<=5 and rating >0):
                rev.message = message ;
                rev.rating = rating;
                rev.number = number;
                #rev.restaurant.capacity
                rev.restaurant.rate = rev.rating

                rev.restaurant.save()
                rev.save()

                print("message:",rev.message," rating:", rating)

                restaurant1 = Review.objects.filter(number=number)
                viewedrestaurants = _check_session(request)
                context = {
                    'details': rev.restaurant,
                    'msg': restaurant1,
                    'viewedrestaurants': viewedrestaurants
                }
                return render(request, 'forkilla/details.html', context)
            else :
                form = ReviewForm()
                form.initial['number'] = r
                form.initial['user'] = request.user
                error = True
                context = {
                    'form': form,
                    'errors' : error,
                }
                return render(request, 'forkilla/review.html', context)

    else:
        form = ReviewForm()
        form.initial['number'] = r
        form.initial['user'] = request.user
        context = {
            'form' : form,
        }
        return render(request,'forkilla/review.html',context)

@login_required(login_url='login')
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user ).order_by('day')
    reservesHoy = []
    reservespasades = []
    for i in reservations:
        print (i.get_human_slot()," : ", i.day," : ",datetime.datetime.now())
        if(i.day.__eq__(datetime.datetime.now())):
            print("yups")
            reservesHoy.append(i)
        else:
            reservespasades.append(i)

    print(reservations)
    context = {
        'reservations': reservations,
        'reservesHoy':reservesHoy,
        'reserves':reservespasades

    }
    return render(request, 'forkilla/reservationlist.html', context)

@login_required
def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse("home"))

def delete(request,id):
    Reservation.objects.get(id=id).delete()
    return restaurants(request)


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Restaurants to be viewed or edited.
    """
    queryset = Restaurant.objects.all().order_by('category')
    serializer_class = RestaurantSerializer


    def get_queryset(self):
        
        category = self.request.query_params.get('category', None)
        is_new = self.request.query_params.get('is_new', None)
        #return Restaurant.objects.filter(category=category,city=city)
        
        
        #is_new = self.request.query_params.get('new', None)
        price = self.request.query_params.get('price', None)
        
        if category and not is_new and not price:
            return Restaurant.objects.filter(category=category)

        if not category and is_new and not price:
            return Restaurant.objects.filter(city=is_new)

        if not category and not is_new and price:
            return Restaurant.objects.filter(price_average=price)

        if category and is_new and not price:
            return Restaurant.objects.filter(category=category, city=is_new)

        if category and not is_new and price:
            return Restaurant.objects.filter(category=category, price_average=price)

        if not category and is_new and price:
            return Restaurant.objects.filter(city=is_new, price_average=price)

        if category and is_new and price:
            return Restaurant.objects.filter(category=category, city=is_new, price_average=price)

        return Restaurant.objects.all()

    """
    ********************* Comparator *********************
    """

def comparator(request, ips):
    context = {
        'ips': ips,
        'categories': restaurants
    }

    return render(request, "forkilla/comparator.html", context)

def api_restaurants(request):
    restaurants_by_city = Restaurant.objects.filter(is_promot="True")
    promoted = True


    context = {

        'restaurants': restaurants_by_city,
        'promoted': promoted,

    }
    return render(request, 'forkilla/restaurants.html', context)



