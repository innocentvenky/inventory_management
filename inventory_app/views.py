from django.shortcuts import render
from django.core.cache import cache
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated
from . models import Items
from . serializers import RegisterSerializer,Loginserializer,Userserializer,Item_serializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response   
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
from rest_framework import status

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes=(AllowAny,)
    serializer_class= RegisterSerializer
class LoginView(generics.GenericAPIView):
    serializer_class=Loginserializer
    def post(self,request,*args,**kwargs):
        username_1=request.data.get('username')
        password_1=request.data.get('password')
        user=authenticate(username=username_1,password=password_1)
        print(user)
        if user is not None:
            print("user exites")
            refresh=RefreshToken.for_user(user)
            user_serializer=Userserializer(user)
            return Response({
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'user': user_serializer.data
            }
            )
        else:
            return Response({'Invalid/details'})
class CreateItem(generics.GenericAPIView,CreateModelMixin):
    queryset=Items.objects.all()
    serializer_class=Item_serializer
    permission_classes =[IsAuthenticated]
    def post(self,request,*args,**kwargs):
        name=request.data.get('name')
        if Items.objects.filter(name=name).exists():
             return Response(
                {"error": "Item already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self.create(request,*args,**kwargs)
class RetrieveItem(generics.GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset=Items.objects.all()
    serializer_class=Item_serializer
    permission_classes =[IsAuthenticated]
    def get(self,request,*args,**kwargs):
        item_id=kwargs.get('pk')
        cache_key=f"item_{item_id}"
        cached_item=cache.get(cache_key)
        if cached_item:
            return Response(cached_item, status=status.HTTP_200_OK)
        
        # If not in cache, retrieve it from the database
        try:
            item = Items.objects.get(pk=item_id)
        except Items.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the item
        serializer = self.get_serializer(item)
        
        # Cache the item for future requests (e.g., cache for 60 minutes)
        cache.set(cache_key, serializer.data, timeout=3600)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #Update the Items
    def put(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        print(item_id)
        cache_key = f"item_{item_id}"
        
        try:
            item = Items.objects.get(pk=item_id)
        except Items.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        response = self.update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the cache after updating
            cache.delete(cache_key)
            return Response({'message': 'successfully updated'}, status=status.HTTP_200_OK)
        
    # deleting Items
    def delete(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        cache_key = f"item_{item_id}"

        try:
            item = Items.objects.get(pk=item_id)
        except Items.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        response = self.destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            # Invalidate the cache after deletion
            cache.delete(cache_key)
            return Response({'message': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
    

    
