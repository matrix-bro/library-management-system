from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from django.urls import reverse
from rest_framework import status

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = {'name': 'Test User', 'email': 'test@example.com', 'membership_date': '2024-01-31', 'password': 'testpassword', 'password2': 'testpassword'}
    
    def test_user_cannot_register_with_same_email(self):
        url = reverse('register')

        response = self.client.post(url, self.user1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # testing with same email
        response = self.client.post(url, self.user1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)     # throws HTTP_400_BAD_REQUEST

        self.assertEqual(User.objects.count(), 1)

    def test_register_user(self):
        url = reverse('register')

        response = self.client.post(url, self.user1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['email'], 'test@example.com')
        self.assertEqual(User.objects.count(), 1)

    def test_get_all_users(self):
        url = reverse('users')
        
        # creating and authenticating a user
        user = User.objects.create_user(name=self.user1['name'], email=self.user1['email'], membership_date=self.user1['membership_date'], password=self.user1['password'])
        self.client.force_authenticate(user=user)

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_by_id(self):
        user = User.objects.create_user(name=self.user1['name'], email=self.user1['email'], membership_date=self.user1['membership_date'], password=self.user1['password'])
        
        url = reverse('user_details', args={user.user_id})

        self.client.force_authenticate(user=user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')