# Uncomment the following imports before adding the Model code
# import sys

from django.db import models
# from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.TextField()
    is_luxury = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    type_choices = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
        ('COMPACT', 'Compact'),

    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50)
    type = models.CharField(
        max_length=10, choices=type_choices, default='SEDAN')
    year = models.IntegerField(default=2023,
                               validators=[
                                   MinValueValidator(2015),
                                   MaxValueValidator(2023)
                               ])

    def __str__(self):
        return str(self.year) + " " + self.name
