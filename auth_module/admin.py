from django.contrib import admin

from auth_module.models import AuthUser, Trip, TripWayPointData, Sector, Bus, Driver, ContactPerson, Coordinates,\
    WayPoint, ServiceHistory, Route
# Register your models here.

admin.site.register(AuthUser)
admin.site.register(Trip)
admin.site.register(TripWayPointData)
admin.site.register(Sector)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(ContactPerson)
admin.site.register(Coordinates)
admin.site.register(WayPoint)
admin.site.register(ServiceHistory)
admin.site.register(Route)