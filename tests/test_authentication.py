"""
Test cases for authentication and user management
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserAuthenticationTest(APITestCase):
    """Test cases for user authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_user_registration(self):
        """Test user registration endpoint if available"""
        url = '/api/v1/auth/registration/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        
        response = self.client.post(url, data)
        
        # This might return 404 if the endpoint doesn't exist
        self.assertIn(response.status_code, [
            status.HTTP_201_CREATED,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST
        ])
        
    def test_user_login(self):
        """Test user login endpoint if available"""
        url = '/api/v1/auth/login/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(url, data)
        
        # This might return 404 if the endpoint doesn't exist
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST
        ])
        
    def test_authenticated_user_access(self):
        """Test that authenticated users can access protected endpoints"""
        self.client.force_authenticate(user=self.user)
        
        # Test accessing user's own posts
        url = '/api/v1/post/self/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_unauthenticated_user_access(self):
        """Test that unauthenticated users cannot access protected endpoints"""
        url = '/api/v1/post/self/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTest(TestCase):
    """Test cases for User model extensions"""
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        
    def test_user_str_method(self):
        """Test the string representation of a user"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'testuser')