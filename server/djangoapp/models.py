from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(blank=False, max_length=50)
    description = models.CharField(null=True, max_length=200)

    def __str__(self):
        description = "No Description" if self.description == "" else "Description: " + self.description
        return "Name: " + self.name + ", " + description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = "Sedan"
    SUV = "SUV"
    WAGON = "Wagon"
    SPORT = "Sport"
    TRUCK = "Truck"
    MINIVAN = "Minivan"
    COUPE = "Coupe"
    OTHER = "Other"

    CAR_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon"),
        (SPORT, "Sport"),
        (TRUCK, "Truck"),
        (MINIVAN, "Minivan"),
        (COUPE, "Coupe"),
        (OTHER, "Other"),
    ]
    
    name = models.CharField(max_length=50, blank=False)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    type = models.CharField(choices=CAR_CHOICES, max_length=50, blank=False)
    year = models.DateField()

    def __str__(self):
        return "Car Make: " + self.make + ", Model: " + self.name + ", Year: " + self.year + ", Type: " + self.type


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id  
        self.name = name  
        self.purchase = purchase  
        self.purchase_date = purchase_date
        self.review = review  
        self.sentiment = sentiment  

    def __str__(self):
        return "Name: " + self.name + " Review: " + self.review