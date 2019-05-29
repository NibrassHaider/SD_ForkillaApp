from django.conf.urls import url
from django.urls import include

from forkilla import views

listOfAddresses = ["161.116.56.65","161.116.56.165"]

urlpatterns = [
    url(r'^comparator/$', views.comparator, kwargs={'ips': listOfAddresses}, name='comparator'),

    #url(r'^restaurants',views.api_restaurants,name='re'),
    #url(r'^$', views.index, name='index'),
    #url(r'^rest/(?P<category>.*)',views.RestaurantViewSet,name='rest'),
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^index/$', views.index, name='index'),
    url(r'^reservationlist/$', views.my_reservations, name='reservationlist'),
    url(r'^restaurants/$', views.restaurants, name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),

    url(r'^all_restaurants/$', views.all_restaurants, name='all_restaurants'),

    url(r'^restaurant/(?P<restaurant_number>.*)',views.details, name='details'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$',views.restaurants,name='restaurants'),
    url(r'^restaurants/(?P<city>.*)/(?P<category>.*)/(?P<menu_description>.*)$',views.restaurants,name='restaurants'),
    url(r'^reservation/$', views.reservation, name='reservation'),
    url(r'^reservation/checkout/$', views.checkout, name='checkout'),
    url(r'^review/(?P<restaurant_number>.*)', views.review, name='review'),
    url(r'^delete/(?P<id>.*)',views.delete,name='delete')
]