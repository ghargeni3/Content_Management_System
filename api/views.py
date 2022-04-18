
from http.client import UNAUTHORIZED
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http.response import Http404
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (
    AuthUserRegistrationSerializer,
    AuthUserLoginSerializer,
    UserListSerializer,
    ContentSerializer,
    ContentListSerializer
)

from .models import Content, User
import pdb

class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

class AuthUserLoginView(APIView):
    serializer_class = AuthUserLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }

            return Response(response, status=status_code)

class UserListView(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request._user
        
        if user.role != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'users': serializer.data

            }
            return Response(response, status=status.HTTP_200_OK)

class ContentRegistrationView(APIView):
    serializer_class = ContentSerializer
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        user = request._user
        try:
            request.data._mutable = True
        except:
            pass
        request.data['author'] = user.email
        try:
            if '.pdf' not in request.data['document'].name:
                return Response({
                    'success': True,
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'message': 'Document type must in PDF format',
                })
        except Exception as e:
            print("Exception : ", e)

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Content successfully Added!',
                'content': serializer.data
            }

            return Response(response, status=status_code)

class ContentListView(APIView):

    serializer_class = ContentListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, uid=None, format=None):
        user = request._user
        if user.role == 1:
            if uid:
                try:
                    contents = Content.objects.get(uid=uid)
                    serializer = self.serializer_class(contents)
                except Content.DoesNotExist:
                    raise Http404
            else:
                contents = Content.objects.all()
                serializer = self.serializer_class(contents, many=True)
        else:
            if uid:
                try:
                    contents = Content.objects.filter(uid=uid)&Content.objects.filter(author=user.email)
                    serializer = self.serializer_class(contents, many=True)
                except Content.DoesNotExist:
                    raise Http404
            else:
                contents = Content.objects.filter(author=user.email)
                serializer = self.serializer_class(contents, many=True)
            
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched contents',
            'contents': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)
    
    def put(self, request, uid=None, format=None):
        user = request._user
        try:
            content_to_update = Content.objects.get(uid=uid)
            serializer = self.serializer_class(instance=content_to_update,data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
        except Content.DoesNotExist:
                    raise Http404

        if '.pdf' not in request.data['document'].name:
            return Response({
                'success': True,
                'statusCode': status.HTTP_400_BAD_REQUEST,
                'message': 'Document type must in PDF format',
            })
        if user.role == 1 or content_to_update.__dict__['author'] == user.email:
            serializer.save()

            return Response({
            'success': True,
            'statusCode': status.HTTP_200_OK,
            'message': 'Content Updated Successfully',
            'contents': serializer.data
        })
        else:
            return Response({
                'success': True,
                'statusCode': status.HTTP_401_UNAUTHORIZED,
                'message': 'Your not authorized to update another authors content',
            })  
    
    def delete(self, request, uid, format=None):
        user = request._user
        content_to_delete =  Content.objects.get(uid=uid)
        serializer = self.serializer_class(content_to_delete)

        if user.role == 1 or serializer.data['author'] == user.email:
            content_to_delete.delete()

            return Response({
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Content Deleted Successfully',
            })
        else:
            return Response({
                'success': True,
                'statusCode': status.HTTP_401_UNAUTHORIZED,
                'message': 'Your not authorized to delete another authors content',
            })

class ContentSearchView(APIView):
    
    serializer_class = ContentListSerializer
    permission_classes = (AllowAny,)

    def get(self, request, key=None):
        contents = Content.objects.filter(
            Q(title__icontains=key) | 
            Q(body__icontains=key) | 
            Q(summury__icontains=key) | 
            Q(categories__icontains=key)
        )
        serializer = self.serializer_class(contents, many=True)
        return Response({
                'success': True,
                'statusCode': status.HTTP_200_OK,
                'message': 'Search Result',
                'user': serializer.data
            })
        