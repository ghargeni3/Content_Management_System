from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Content

class AuthUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'role',
            'full_name',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'pincode'
        )

    def validate(self, data):
        if data.get('email', None) is None:
            raise serializers.ValidationError("Email is required")

        password = str(data.get('password', None))
        if data.get('password', None) is not None:
            if len(password)<7 or data.get('password', None) is None:
                raise serializers.ValidationError("Password is too short(Min 8 characters required!)")
            elif not any(char.isupper() for char in password):
                raise serializers.ValidationError('Password should have at least one uppercase letter')
            elif not any(char.islower() for char in password):
                raise serializers.ValidationError('Password should have at least one lowercase letter')
        else:
            raise serializers.ValidationError("Password is too short(Min 8 characters required!)")
            
        
        if data.get('role', None)  is None:
            raise serializers.ValidationError("Role is required")
        
        if data.get('full_name', None) is None:
            raise serializers.ValidationError("Full Name is required")
        
        if data.get('phone', None) is None:
            raise serializers.ValidationError("Phone is required")
        
        if len(str(data.get('pincode', None)))>6 or data.get('pincode', None) is None:
            raise serializers.ValidationError("Pincode must be six digit")

        return data
    
    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user

class AuthUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'uid',
            'full_name',
            'email',
            'role',
            'phone',
            'address',
            'city',
            'state',
            'country',
            'pincode'
        )

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content

        fields = (
            'title',
            'body',
            'summury',
            'document',
            'categories',
            'author'
        )

    def create(self, validated_data):
        content_data = Content.objects.create(**validated_data)
        return content_data

class ContentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'uid',
            'title',
            'body',
            'summury',
            'categories',
            'author',
            'document'
        )

