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


# <HINT> Create a plain Python class `DealerReview` to hold review data
