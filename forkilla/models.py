from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        first_name = models.CharField(default="Nibrass ",max_length=30)
        last_name = models.CharField(default="Haider ",max_length=150)
        email = models.EmailField(default="user@gmail.com") # name that appears on screen (complementary username)
        birthday = models.DateField(auto_now=False, auto_now_add=False,null=True)


        """"@receiver(post_save, sender=User)
        def update_user_profile(sender, instance, created, **kwargs):
                if created:
                        Profile.objects.create(user=instance)
                instance.profile.save()"""


# Restaurant Model Class
class Restaurant(models.Model):
        CATEGORIES = (
        ("Rice", "Rice"),
        ("Fusi", "Fusion"),
        ("BBQ", "Barbecue"),
        ("Chin", "Chinese"),
        ("Medi", "Mediterranean"),
        ("Crep", "Creperie"),
        ("Hind", "Hindu"),
        ("Japa", "Japanese"),
        ("Ital", "Italian"),
        ("Mexi", "Mexican"),
        ("Peru", "Peruvian"),
        ("Russ", "Russian"),
        ("Turk", "Turkish"),
        ("Basq", "Basque"),
        ("Vegy", "Vegetarian"),
        ("Afri", "African"),
        ("Egyp", "Egyptian"),
        ("Grek", "Greek"))

        _d_categories = dict(CATEGORIES);

        #user = models.ForeignKey(User, on_delete=models.CASCADE)
        restaurant_number = models.CharField(max_length=8)

        name = models.CharField(max_length=50)
        menu_description = models.CharField(max_length=80)
        price_average = models.DecimalField(max_digits=5, decimal_places=2)
        is_promot = models.BooleanField()
        rate = models.DecimalField(max_digits=3, decimal_places=1)
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=50)
        country = models.CharField(max_length=50)
        #featured_photo = models.ImageField()
        featured_photo = models.CharField(max_length=250)
        category = models.CharField(max_length=5, choices=CATEGORIES)
        capacity = models.PositiveIntegerField()

        def get_human_category(self):
            return self._d_categories[self.category]


        def get_menu(self):
                return self.menu_description

        def get_data(self):

             return ('Restaurant Number : ' + self.restaurant_number + '\n Name : ' + self.name + '\n Menu Description :'
                     + self.menu_description + '\n Price Average : '+ str(self.price_average) + '\n Promoted : ' +
                     str(self.is_promot) + '\n  Rate : ' + str(self.rate) + '\n Adress : '+self.address +
                     '\n City : '+ self.city + '\n Country' + self.country
                     + '\n Category : ' + self.category)

        def __str__(self):
            return ('[**Promoted**]' if self.is_promot else '') + "[" + self.category + "] " \
             "[" + self.restaurant_number + "] " + self.name + " - " + self.menu_description + " (" + str(
              self.rate) + ")" \
             ": " + str(self.price_average) + u" €"


# Reservation of a restaurant class model
class Reservation(models.Model):

        SLOTS = (
        ("morning_first", "12h00"),
        ("morning_second", "13h00"),
        ("morning_third", "14h00"),
        ("morning_fourth", "15h00"),
        ("evening_first", "20h00"),
        ("evening_second", "21h00"),
        ("evening_third", "22h00"),
        )

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        _d_slots = dict(SLOTS)
        id = models.AutoField(primary_key=True)
        restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
        day = models.DateField(default=datetime.now)
        time_slot = models.CharField(max_length=15, choices=SLOTS)
        num_people = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

        def get_human_slot(self):
                return self._d_slots[self.time_slot]

# To save in session the list of 5 restaurants which are visited the most
class ViewedRestaurants(models.Model):
   		id_vr = models.AutoField(primary_key=True)
   		restaurant = models.ManyToManyField(Restaurant)

class Review(models.Model):
        restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,null=True)
        #reservation = models.ForeignKey(Reservation,on_delete=models.CASCADE,null=True)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        number = models.CharField(max_length=8,default="")
        message = models.TextField()
        rating = models.PositiveIntegerField()
        #restaurant = models.ManyToManyField(Restaurant, null=True)





