from rest_framework import serializers
from .models import User, Client, Professional
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    card_number = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'role',
            'full_name', 'birth_date', 'phone', 'card_number'
        ]

    def create(self, validated_data):

        if User.objects.filter(email=validated_data['email']).exists():
             raise serializers.ValidationError("Email already registered.")
    
        role = validated_data.get('role')
        card_number = validated_data.pop('card_number', None)
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        if role == 'client':
            Client.objects.create(user=user)
        elif role == 'professional':
            if not card_number:
                raise serializers.ValidationError("Card number is required for professionals.")
            Professional.objects.create(user=user, card_number=card_number)

        return user


class ProfessionalSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Professional
        fields = ['id', 'full_name', 'email', 'card_number', 'status']
        read_only_fields = ['status']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if user.is_professional():
            professional = getattr(user, 'professional_profile', None)
            if professional and professional.status != 'approved':
                raise serializers.ValidationError("Professional account is not approved yet.")

        refresh = RefreshToken.for_user(user)

        return {
            'email': user.email,
            'role': user.role,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
