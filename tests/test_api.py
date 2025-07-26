"""
Basic API tests for the Reddit clone application
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.posts.models import Post


class PostAPITest(TestCase):
    """Test cases for Post API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_get_posts_list(self):
        """Test retrieving posts list"""
        # Create a test post
        Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        url = reverse('posts-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_create_post_authenticated(self):
        """Test creating a post when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        url = reverse('posts-list')
        data = {
            'title': 'New Test Post',
            'content': 'New test content'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        
    def test_create_post_unauthenticated(self):
        """Test creating a post when not authenticated"""
        url = reverse('posts-list')
        data = {
            'title': 'New Test Post',
            'content': 'New test content'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)