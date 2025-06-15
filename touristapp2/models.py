from django.db import models

class Membershipmodel(models.Model):
    COUNTRY_CHOICES = (('India', 'India'), ('Outside India', 'Outside India'))
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES, default='India')
    special_request = models.TextField()

class Bookingmodel(models.Model):
    LOCATION_CHOICES = (
        ('Janjehli Resort', 'Janjehli Resort'),
        ('Kandaghat Shimla Resort', 'Kandaghat Shimla Resort'),
        ('Kanatal Resort', 'Kanatal Resort'),
        ('Mussoorie Resort', 'Mussoorie Resort'),
    )
    PERSONS_CHOICES = ((1, 1), (2, 2), (3, 3), (4, 4))
    MEMBERSHIP_CHOICES = (('Yes', 'Yes'), ('No', 'No'))
    ROOM_CHOICES = (('S', 'Studio Apartment'), ('1', '1-Bedroom Apartment'), ('2', '2-Bedroom Apartment'))

    name = models.CharField(max_length=30)
    email = models.EmailField()
    check_in_date_and_time = models.DateTimeField()
    check_out_date_and_time = models.DateTimeField()
    destination = models.CharField(max_length=30, choices=LOCATION_CHOICES)
    no_of_persons = models.IntegerField(choices=PERSONS_CHOICES)
    have_you_availed_membership = models.CharField(max_length=30, choices=MEMBERSHIP_CHOICES)
    type_of_room = models.CharField(max_length=30, choices=ROOM_CHOICES)

class Roomsmodel(models.Model):
    name = models.CharField(max_length=30)
    studio = models.IntegerField()
    onebed = models.IntegerField()
    twobed = models.IntegerField()

class Feedbackmodel(models.Model):
    fb = models.TextField(max_length=300)

# models.py
class Resort(models.Model):
    name = models.CharField(max_length=100)
    resort_type = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image_url = models.URLField(null=False, blank=False)  # <- enforce required
  # ✅ Add this

    def __str__(self):
        return self.name
