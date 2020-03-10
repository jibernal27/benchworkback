

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.db import transaction


from .serializers import BaseUserSerializer, UserSerializer, PlaceSerializer, FileSerializer, LanguageSerializer
from  .models import BaseUser, Place, File, User, Language

# Create your views here.


@api_view(['POST'])
@transaction.atomic
def sign_up_user(request):
    user_serializer = UserSerializer(data=request.data, context={'request': request})
    base_user_serializer = BaseUserSerializer(data=request.data, context={'request': request})
    if user_serializer.is_valid(raise_exception=True) and base_user_serializer.is_valid(raise_exception=True):
        data = user_serializer.validated_data
        user_data = base_user_serializer.validated_data
        base_user = BaseUser.objects.create_user(user_data['username'], user_data['password'])
        user = User(base_user=base_user, **data)
        user.save()
        refresh = RefreshToken.for_user(base_user)
        return Response({'refresh': str(refresh),'access': str(refresh.access_token)},status=status.HTTP_201_CREATED)



def update_profile(request):
    serializer = UserSerializer(data=request.data, instance=request.user.user, context={'request': request}, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)


def get_profile(request):
    serializer = UserSerializer(instance=request.user.user, context={'request': request})
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'POST':
        return update_profile(request)
    return get_profile(request)
@api_view(['GET'])
def app_init_data(request):
    serializer = LanguageSerializer(Language.objects.all(), many=True)
    return Response({'languages':serializer.data})

class PlacesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PlaceSerializer

    def get_queryset(self):
        return Place.objects.filter(user=self.request.user.user).order_by('-date_init', '-date_end')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user)

class FilesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter(user=self.request.user.user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.user)