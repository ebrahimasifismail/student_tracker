from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from auth.serializers import UserSerializer
from django.contrib.auth.models import User


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
        import pdb; pdb.set_trace()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_201_CREATED)