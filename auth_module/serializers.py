from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from auth_module.models import Sector, Bus, Route, Trip, TripWayPointData, WayPoint, Coordinates, Driver, ContactPerson
from auth_module.models import AuthUser


class ContactPersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPerson
        fields = "__all__"

class CoordinatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coordinates
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuthUser
        fields = ('id', 'username', 'email', 'password', 'user_type')


class SectorSerializer(serializers.ModelSerializer):
    contact_person = ContactPersonSerializer()

    class Meta:
        model = Sector
        fields = "__all__"


class CommonSectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sector
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):
    sector_id = SectorSerializer()

    class Meta:
        model = Bus
        fields = "__all__"


class CommonBusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = "__all__"


class DriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    sector_id = SectorSerializer
    start_point_coordinates = CoordinatesSerializer()
    destination_coordinates = CoordinatesSerializer()

    class Meta:
        model = Route
        fields = "__all__"


class CommonRouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = "__all__"


class WayPointSerializer(serializers.ModelSerializer):
    way_point_coordinates = CoordinatesSerializer()

    class Meta:
        model = WayPoint
        fields = "__all__"


class CommonWayPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = WayPoint
        fields = "__all__"


class TripSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = "__all__"


class TripWayPointDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripWayPointData
        fields = "__all__"


class ListTripWayPointDataSerializer(serializers.ModelSerializer):
    way_point = WayPointSerializer()

    class Meta:
        model = TripWayPointData
        fields = "__all__"


class ActiveTripSerializer(serializers.ModelSerializer):
    way_points = serializers.SerializerMethodField('get_way_points')
    trip_way_points = serializers.SerializerMethodField('get_trip_way_points')
    bus = BusSerializer()
    driver = DriverSerializer()
    route = RouteSerializer()

    def get_way_points(self, obj):
        way_points = WayPoint.objects.filter(route=obj.route.id).order_by("sort_order")
        serializer = WayPointSerializer(way_points, many=True)
        return serializer.data

    def get_trip_way_points(self, obj):
        way_points = TripWayPointData.objects.filter(trip=obj.id).order_by("sort_order")
        serializer = ListTripWayPointDataSerializer(way_points, many=True)
        return serializer.data

    class Meta:
        model = Trip
        fields = "__all__"