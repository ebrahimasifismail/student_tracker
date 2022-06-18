from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from auth_module.serializers import UserSerializer, SectorSerializer, BusSerializer, RouteSerializer, \
    ActiveTripSerializer, TripSerializer, TripWayPointDataSerializer, CommonWayPointSerializer, CommonSectorSerializer,\
    CommonRouteSerializer, CommonBusSerializer, DriverSerializer, ContactPersonSerializer
from django.contrib.auth.models import User
from auth_module.models import Sector, Bus, Route, Trip, WayPoint, TripWayPointData, Driver, ContactPerson
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from auth_module.utils import return_success_response, return_failure_response


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):


    @classmethod
    def get_token(cls, user):
        # import pdb; pdb.set_trace()
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['id'] = user.id
        # ...

        return token

    def validate(self, attrs):
        import pdb; pdb.set_trace()
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['username'] = self.user.username
        data['id'] = self.user.id
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type
        return data


class MyTokenObtainPairView(TokenObtainPairView):
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
                                               token=request.auth.token,
                                               message="User created Successfully"
                                               )
        else:
            return return_failure_response(data=serializer.data,
                                           token=request.auth.token,
                                           message=str(serializer.errors)
                                           )


class ListSectors(generics.ListAPIView):
    """
    Creates the user.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        queryset = self.get_queryset()
        serializer = SectorSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token,
                                       message="Sectors listed Successfully"
                                       )


class ListBusesBySector(generics.ListAPIView):
    """
    Lists buses by sector_id.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        sector_id -- Unique identifier for Sector
        """
        import pdb; pdb.set_trace()
        sector_id = kwargs.get("id")
        queryset = self.get_queryset().filter(id=sector_id)
        serializer = BusSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token,
                                       message=f"Buses for sector {sector_id} listed Successfully"
                                       )


class ListRoutesBySector(generics.ListAPIView):
    """
    Lists buses by sector_id.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        sector_id -- Unique identifier for Sector
        """
        sector_id = kwargs.get("id")
        queryset = self.get_queryset().filter(id=sector_id)
        serializer = RouteSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token,
                                       message=f"Routes for sector {sector_id} listed Successfully"
                                       )


class ListActiveTripByBus(generics.ListAPIView):
    """
    List active trips by bus_id
    """
    queryset = Trip.objects.all()
    serializer_class = ActiveTripSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        param1 -- A first parameter
        param2 -- A second parameter
        """
        sector_id = kwargs.get("id")
        queryset = self.get_queryset().filter(id=sector_id, status="ACTIVE")
        serializer = ActiveTripSerializer(queryset, many=True)
        return return_success_response(data=serializer.data,
                                       token=request.auth.token,
                                       message="User created Successfully"
                                       )


class ListCreateTripView(generics.ListCreateAPIView):
    """
    List active trips by bus_id
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyTripView(generics.RetrieveUpdateDestroyAPIView):
    """
    List active trips by bus_id
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]


class ListCreateTripWayPointView(generics.ListCreateAPIView):
    """
    List active trips by bus_id
    """
    queryset = TripWayPointData.objects.all()
    serializer_class = TripWayPointDataSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyTripWayPointView(generics.RetrieveUpdateDestroyAPIView):
    """
    List active trips by bus_id
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
    List Create sector
    """
    queryset = WayPoint.objects.all()
    serializer_class = CommonWayPointSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyWayPointView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Sector
    """
    queryset = WayPoint.objects.all()
    serializer_class = CommonWayPointSerializer
    permission_classes = [IsAuthenticated]


class ListCreateRouteView(generics.ListCreateAPIView):
    """
    List Create sector
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
    List Create sector
    """
    queryset = Bus.objects.all()
    serializer_class = CommonBusSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyBusView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Sector
    """
    queryset = Bus.objects.all()
    serializer_class = CommonBusSerializer
    permission_classes = [IsAuthenticated]


class ListCreateDriverView(generics.ListCreateAPIView):
    """
    List Create sector
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyDriverView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Sector
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]


class ListCreateContactPersonView(generics.ListCreateAPIView):
    """
    List Create sector
    """
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [IsAuthenticated]


class RetrieveUpdateDestroyContactPersonView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve Update, Destroy Sector
    """
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer
    permission_classes = [IsAuthenticated]