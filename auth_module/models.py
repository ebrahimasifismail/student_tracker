from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Coordinates(models.Model):
    name = models.CharField(max_length=150, default="place_name", blank=True, null=True)
    lat = models.DecimalField(decimal_places=6, max_digits=12, blank=True, null=True)
    long = models.DecimalField(decimal_places=6, max_digits=12, blank=True, null=True)


class AuthUser(AbstractUser):

    USER_TYPES = (
        ('driver', 'Driver'),
        ('pass', 'Passenger'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)


class ContactPerson(models.Model):

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    address_line_one = models.CharField(max_length=150, blank=True, null=True)
    address_line_two = models.CharField(max_length=150, blank=True, null=True)
    designation = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.first_name

    class Meta:
        ordering = ["first_name"]
        verbose_name_plural = "contact_persons"


class Sector(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    type = models.CharField(max_length=150, blank=True, null=True)
    address_line_one = models.CharField(max_length=150, blank=True, null=True)
    address_line_two = models.CharField(max_length=150, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    contact_person = models.ForeignKey('ContactPerson', on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "sectors"


class ServiceHistory(models.Model):
    date_of_service = models.DateTimeField()
    issue = models.CharField(max_length=150, blank=True, null=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    service_cost = models.CharField(max_length=150, blank=True, null=True)


    def __str__(self):
        return self.date_of_service

    class Meta:
        ordering = ["date_of_service"]
        verbose_name_plural = "service_histories"


class Bus(models.Model):

    sector_id = models.ForeignKey('Sector', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True, null=True)
    registration = models.CharField(max_length=150, blank=True, null=True)
    registration_validity = models.DateTimeField(blank=True, null=True)
    manufacturer = models.CharField(max_length=150, blank=True, null=True)
    model = models.CharField(max_length=150, blank=True, null=True)
    year_of_manufacturer = models.IntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True) # number of seats
    service_history = models.ManyToManyField('ServiceHistory', blank=True)
    mileage = models.DecimalField(decimal_places=3, max_digits=6, blank=True, null=True)
    insurance = models.CharField(max_length=150, blank=True, null=True)
    insurance_validity = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.registration

    class Meta:
        ordering = ["registration"]
        verbose_name_plural = "buses"


class Driver(models.Model):

    sector_id = models.ForeignKey('Sector', on_delete=models.CASCADE)
    user = models.ForeignKey('AuthUser', on_delete=models.CASCADE)
    date_of_join = models.DateTimeField(blank=True, null=True)
    phone = models.CharField(max_length=150, blank=True, null=True)
    address_line_one = models.CharField(max_length=150, blank=True, null=True)
    address_line_two = models.CharField(max_length=150, blank=True, null=True)
    emergency_contact = models.ForeignKey('ContactPerson', on_delete=models.CASCADE)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ["user"]
        verbose_name_plural = "drivers"


class Route(models.Model):

    sector_id = models.ForeignKey('Sector', on_delete=models.CASCADE)
    start_point = models.CharField(max_length=150, blank=True, null=True)
    destination = models.CharField(max_length=150, blank=True, null=True)
    start_point_coordinates = models.ForeignKey('Coordinates',
                                                on_delete=models.CASCADE,
                                                related_name="start_point_coordinates")
    destination_coordinates = models.ForeignKey('Coordinates',
                                                on_delete=models.CASCADE,
                                                related_name="destination_coordinates")

    def __str__(self):
        return f"{self.start_point}_{self.destination}"

    class Meta:
        verbose_name_plural = "routes"


class WayPoint(models.Model):

    way_point_name = models.CharField(max_length=150, blank=True, null=True)
    way_point_coordinates = models.ForeignKey('Coordinates', on_delete=models.CASCADE)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    sort_order = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return self.way_point_name

    class Meta:
        ordering = ["way_point_name"]
        verbose_name_plural = "way_points"


class TripWayPointData(models.Model):

    trip = models.ForeignKey('Trip', on_delete=models.CASCADE)
    way_point = models.ForeignKey('WayPoint', on_delete=models.CASCADE)
    arrival_time = models.DateTimeField(blank=True, null=True)
    sort_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Trip: {str(self.trip.id)} WayPoint: {self.way_point.way_point_name}"

    class Meta:
        ordering = ["trip"]
        verbose_name_plural = "trip_meta_data"


class Trip(models.Model):

    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.CASCADE)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.bus}_{self.id}"

    class Meta:
        verbose_name_plural = "trips"
