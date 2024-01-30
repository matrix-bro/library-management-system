from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers, permissions
from django.contrib.auth import get_user_model
User = get_user_model()
from app.services.user_services import create_user_account
from rest_framework.generics import ListAPIView, RetrieveAPIView

class RegisterUser(APIView):
    """
    API endpoint for user registration.
    """

    class InputSerializer(serializers.ModelSerializer):
        """
        Serializer for input data during user registration.
        """
        class Meta:
            model = User
            fields = ('name', 'email', 'membership_date', 'password', 'password2')

        password = serializers.CharField(write_only=True)
        password2 = serializers.CharField(write_only=True)

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({
                    'error': 'Password fields didnot match.'
                })
            
            attrs.pop('password2')  # After validation, remove password2 from serializers.validated_data
            
            return attrs
        
    def post(self, request):
        """
        Handle user registration POST request.
        """
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # a service for user account creation
        user = create_user_account(**serializer.validated_data)

        response = self.InputSerializer(user)

        return Response({
            'success': 'User account created successfully.',
            'data': response.data,
            'status': status.HTTP_201_CREATED,
        }, status=status.HTTP_201_CREATED)
    

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to display user details
    """
    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'membership_date')

class GetAllUsers(ListAPIView):
    """
    API endpoint to retrieve a list of all regular users.
    - Requires the user to be authenticated.
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer

class GetUserById(RetrieveAPIView):
    """
    API endpoint to retrieve details of a specific regular user by user ID.
    - Requires the user to be authenticated.
    """
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer
