"""student_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from django.urls import path
from django.contrib import admin
from auth_module.views import UserCreate, ListSectors, ListBusesBySector, MyTokenObtainPairView, ListRoutesBySector, \
    ListActiveTripByBus, ListCreateTripView, RetrieveUpdateDestroyTripView, RetrieveUpdateDestroyWayPointView, \
    ListCreateWayPointView, ListCreateRouteView, ListCreateSectorView, ListCreateBusView, \
    RetrieveUpdateDestroyRouteView, RetrieveUpdateDestroySectorView, RetrieveUpdateDestroyBusView, \
    ListCreateTripWayPointView, RetrieveUpdateDestroyTripWayPointView, ListCreateDriverView, \
    RetrieveUpdateDestroyDriverView, ListCreateContactPersonView, RetrieveUpdateDestroyContactPersonView, \
    EndActiveTripView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from rest_framework_simplejwt import views as jwt_views


schema_view = get_schema_view(
   openapi.Info(
      title="Student Tracker API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Your URLs...
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/create-user/', UserCreate.as_view(), name='create-user'),
    path('api/list-sectors/', ListSectors.as_view(), name='list-sectors'),
    path('api/list-buses/sector-id/<int:id>/', ListBusesBySector.as_view(), name='list-buses-by-sector'),
    path('api/active-trip/bus-id/<int:id>/', ListActiveTripByBus.as_view(), name='list-active-trips-by-bus'),
    path('api/list-routes/sector-id/<int:id>/', ListRoutesBySector.as_view(), name='list-routes-by-sector'),
    path('api/trip/', ListCreateTripView.as_view(), name='list-create-trip'),
    path('api/trip/<int:pk>/', RetrieveUpdateDestroyTripView.as_view(), name='retrieve-update-destroy-trip'),
    path('api/way-points/', ListCreateWayPointView.as_view(), name='list-create-update-destry-trip'),
    path('api/way-points/<int:pk>/',
         RetrieveUpdateDestroyWayPointView.as_view(),
         name='list-create-update-destry-trip'),
    path('api/trip-way-points/', ListCreateTripWayPointView.as_view(), name='list-create-update-destry-trip'),
    path('api/trip-way-points/<int:pk>/',
         RetrieveUpdateDestroyTripWayPointView.as_view(),
         name='list-create-update-destry-trip'),
    path('api/route/', ListCreateRouteView.as_view(), name='list-create-route'),
    path('api/route/<int:pk>/',
         RetrieveUpdateDestroyRouteView.as_view(),
         name='retrieve-update-destroy-trip'),
    path('api/sector/', ListCreateSectorView.as_view(), name='list-create-sector'),
    path('api/sector/<int:pk>/',
         RetrieveUpdateDestroySectorView.as_view(),
         name='retrieve-update-destroy-sector'),
    path('api/bus/', ListCreateBusView.as_view(), name='list-create-driver'),
    path('api/bus/<int:pk>/',
         RetrieveUpdateDestroyBusView.as_view(),
         name='retrieve-update-destroy-bus'),
    path('api/driver/', ListCreateDriverView.as_view(), name='list-create-driver'),
    path('api/driver/<int:pk>/',
         RetrieveUpdateDestroyDriverView.as_view(),
         name='retrieve-update-destroy-bus'),
    path('api/contact-person/', ListCreateContactPersonView.as_view(), name='list-create-contact-person'),
    path('api/contact-person/<int:pk>/',
         RetrieveUpdateDestroyContactPersonView.as_view(),
         name='retrieve-update-destroy-contact-person'),
    path('api/end-active-trip/', EndActiveTripView.as_view(), name='end-active-trip'),
]
