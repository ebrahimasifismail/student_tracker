import datetime

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_module.serializers import UserSerializer, SectorSerializer, BusSerializer, RouteSerializer, \
    ActiveTripSerializer, TripSerializer, TripWayPointDataSerializer, CommonWayPointSerializer, CommonSectorSerializer,\
    CommonRouteSerializer, CommonBusSerializer, DriverSerializer, ContactPersonSerializer, EndActiveTripSerializer
from django.contrib.auth.models import User
from auth_module.models import Sector, Bus, Route, Trip, WayPoint, TripWayPointData, Driver, ContactPerson
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from auth_module.utils import return_success_response, return_failure_response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customize JWT Token Response with extra user identifiers
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['id'] = user.id
        # ...

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['id'] = self.user.id
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type
        driver = Driver.objects.filter(user=self.user.id)

        data["driver_sector"] = ""
        data["driver_id"] = ""
        if driver:
            driver = driver.first()

            data["driver_id"] = driver.id
            data["driver_sector"] = driver.sector_id.id
            trip = Trip.objects.filter(driver=driver.id, status="ACTIVE")
            data["trip_bus"] = ""
            data["trip"] = ""
            if trip:
                trip = trip.first()
                data["trip_bus"] = trip.bus.id
                data["trip"] = trip.id
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    """
        Customize JWT Token Response with extra user identifiers
    """
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: MyTokenObtainPairSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserCreate(generics.GenericAPIView):
    """
    Creates the user.
    """
    serializer_class = UserSerializer

    def post(self, request, format='json'):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return return_success_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="User created Successfully"
                                               )
        else:
            return return_failure_response(data=serializer.data,
                                           token=request.auth.token if request.auth else "",
                                           message=str(serializer.errors)
                                           )


class ListSectors(generics.ListAPIView):
    """
    List all sectors.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        queryset = self.get_queryset()
        serializer = SectorSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token if request.auth else "",
                                       message="Sectors listed Successfully"
                                       )


class ListBusesBySector(generics.ListAPIView):
    """
    Lists buses by sector_id.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        sector_id -- Unique identifier for Sector
        """
        sector_id = kwargs.get("id")
        queryset = self.get_queryset().filter(sector_id=sector_id)
        serializer = BusSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token if request.auth else "",
                                       message=f"Buses for sector {sector_id} listed Successfully"
                                       )


class ListRoutesBySector(generics.ListAPIView):
    """
    Lists routes by sector_id.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        sector_id -- Unique identifier for Sector
        """
        sector_id = kwargs.get("id")
        queryset = self.get_queryset().filter(sector_id=sector_id)
        serializer = RouteSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token if request.auth else "",
                                       message=f"Routes for sector {sector_id} listed Successfully"
                                       )


class ListActiveTripByBus(generics.ListAPIView):
    """
    List active trips by bus_id
    """
    queryset = Trip.objects.all()
    serializer_class = ActiveTripSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        bus_id = kwargs.get("id")
        queryset = self.get_queryset().filter(bus=bus_id, status="ACTIVE")
        serializer = ActiveTripSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token if request.auth else "",
                                       message="Active Trips Listed"
                                       )


class ListCreateTripView(generics.ListCreateAPIView):
    """
    List Create trips
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


    def post(self, request, format='json'):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        serializer = self.get_serializer(data=request.data)
        bus_id = request.data.get("bus")
        route_id = request.data.get("route")
        driver_id = request.data.get("driver")

        active_trips = self.get_queryset().filter(bus=bus_id, route=route_id, driver=driver_id,  status="ACTIVE")
        if serializer.is_valid() and not active_trips:
            user = serializer.save()
            if user:
                return return_success_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="Trip created Successfully"
                                               )
        else:
            if active_trips:
                return return_success_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="Active Trip already exists"
                                               )
            else:
                return return_failure_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message=str(serializer.errors)
                                               )



class RetrieveUpdateDestroyTripView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy trips
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


class ListCreateTripWayPointView(generics.ListCreateAPIView):
    """
    List Create Trip Way points
    """
    queryset = TripWayPointData.objects.all()
    serializer_class = TripWayPointDataSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, format='json'):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        return_data = {}
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            trip_id = serializer.data.get("trip")
            trip_obj = Trip.objects.get(id=trip_id)
            bus_id = trip_obj.bus.id
            queryset = Trip.objects.filter(bus=bus_id, status="ACTIVE")
            active_trip_serializer = ActiveTripSerializer(queryset, many=True)
            return_data["trip_way_point"] = serializer.data
            return_data["active_trip_data"] = active_trip_serializer.data
            if user:
                return return_success_response(data=active_trip_serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="Trip Way point created Successfully"
                                               )
        else:
            return return_failure_response(data=serializer.data,
                                           token=request.auth.token if request.auth else "",
                                           message=str(serializer.errors))


class RetrieveUpdateDestroyTripWayPointView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Trip Way points
    """
    queryset = TripWayPointData.objects.all()
    serializer_class = TripWayPointDataSerializer
    permission_classes = [IsAuthenticated]


class ListCreateSectorView(generics.ListCreateAPIView):
    """
    List Create sector
    """
    queryset = Sector.objects.all()
    serializer_class = CommonSectorSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroySectorView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Sector
    """
    queryset = Sector.objects.all()
    serializer_class = CommonSectorSerializer
    permission_classes = [IsAuthenticated]


class ListCreateWayPointView(generics.ListCreateAPIView):
    """
    List Create way points
    """
    queryset = WayPoint.objects.all()
    serializer_class = CommonWayPointSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyWayPointView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Way points
    """
    queryset = WayPoint.objects.all()
    serializer_class = CommonWayPointSerializer
    permission_classes = [IsAuthenticated]


class ListCreateRouteView(generics.ListCreateAPIView):
    """
    List Create route
    """
    queryset = Route.objects.all()
    serializer_class = CommonRouteSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyRouteView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Route
    """
    queryset = Route.objects.all()
    serializer_class = CommonRouteSerializer
    permission_classes = [IsAuthenticated]


class ListCreateBusView(generics.ListCreateAPIView):
    """
    List Create Bus
    """
    queryset = Bus.objects.all()
    serializer_class = CommonBusSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyBusView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Bus
    """
    queryset = Bus.objects.all()
    serializer_class = CommonBusSerializer
    permission_classes = [IsAuthenticated]


class ListCreateDriverView(generics.ListCreateAPIView):
    """
    List Create Driver
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyDriverView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Driver
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]


class ListCreateContactPersonView(generics.ListCreateAPIView):
    """
    List Create Contact Person
    """
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyContactPersonView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Contact Person
    """
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [IsAuthenticated]

class EndActiveTripView(generics.CreateAPIView):
    """
    Retrieve Update, Destroy Contact Person
    """
    queryset = Trip.objects.all()
    serializer_class = EndActiveTripSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            active_trip = self.get_queryset().get(id=serializer.data.get("trip_id"))
            if active_trip:
                active_trip.status="INACTIVE"
                active_trip.end_time = serializer.data.get("end_time")
                active_trip.save()
                return return_success_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="Trip Ended Successfully"
                                               )
            else:
                return return_failure_response(data=serializer.data,
                                               token=request.auth.token if request.auth else "",
                                               message="Active trip not found")

        else:
            return return_failure_response(data=serializer.data,
                                           token=request.auth.token if request.auth else "",
                                           message=str(serializer.errors))