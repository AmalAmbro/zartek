from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import APIException

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.sessions.backends.db import SessionStore

from ride.models import *
from ride.serializers import *
from ride.functions import match_ride_with_driver


# Create your views here.
class UserViewset(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['username', 'email', 'is_driver',]
    search_fields = ['id', 'username', 'email',]
    ordering_fields = ['id', 'username', 'email',]
    pagination_class  = PageNumberPagination

    # user registration endpoint
    @action(detail=False, methods=['post'])
    def register(self, request):
        if request.data.get('username', None) == None:
            return Response({'detail': 'Username cannot be empty'})
        
        if request.data.get('email', None) == None:
            return Response({'detail': 'Email cannot be empty'})

        if request.data.get('password', None) == None:
            return Response({'detail': 'Password cannot be empty'})
        
        try:
            user = User(
                username=request.data.get('username'),
                email=request.data.get('email'),
                first_name=request.data.get('first_name', None),
                last_name=request.data.get('last_name', None),
            )

            user.set_password(request.data.get('password'))
            user.save()

            return Response({'detail': 'Success', 'data': self.serializer_class(user).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e.args[0])
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    # user login endpoint
    @action(detail=False, methods=['post'])
    def login(self, request):
        if request.data.get('username', None) == None:
            return Response({'detail': 'Username cannot be empty'})

        if request.data.get('password', None) == None:
            return Response({'detail': 'Password cannot be empty'})
        
        try:
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                session = SessionStore()
                session['user_id'] = user.id
                session.save()
                return Response({'detail': 'Success', 'sessionId': session.session_key, 'data':UserSerializer(user).data}, status=status.HTTP_200_OK)
            else:
                raise APIException('Invalid Credentials')

        except Exception as e:
            print(e.args[0])
            return Response({'error': e.args[0]})


class RidesViewset(ModelViewSet):
    queryset = Rides.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rider', 'driver', 'status',]
    search_fields = ['id', 'rider', 'driver', 'status',]
    ordering_fields = ['id', 'rider', 'driver', 'status',]
    pagination_class  = PageNumberPagination

    # status updation endpoint
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        instance = self.get_object()
        if request.data.get('status', None) is not None:
            instance.status = request.data.get('status', None)
            instance.save()
            return Response({'detail': 'Status Updated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Status can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
    # ride accept endpoint
    @action(detail=True, methods=['put'])
    def accept_ride(self, request, pk=None):
        instance = self.get_object()
        driver_id = request.data.get('driver', None)
        if driver_id is None:
            return Response({'error': "Driver cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            driver = User.objects.get(id=driver_id, is_driver=True)
            instance.driver = driver
            instance.status = 'accepted'
            instance.save()
            return Response({'detail': 'Success'}, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            print(e.args[0])
            return Response({'error': e.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            print(e.args[0])
            return Response({'error': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def match_driver(self, request, pk=None):
        instance = self.get_object()
        if instance.status in ['requested', 'accepted']:
            driver = match_ride_with_driver(instance)

            if driver is None:
                return Response({'detail': 'No driver found'}, status=status.HTTP_200_OK)

            instance.driver = driver
            instance.save()

            return Response({'detail': 'Driver Matched'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Something went wrong. check ride status again'}, status=status.HTTP_406_NOT_ACCEPTABLE)
