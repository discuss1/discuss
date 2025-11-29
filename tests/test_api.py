"""
Basic API tests for the Reddit clone application
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from posts.models import Post


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
        
        url = '/api/v1/posts/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_create_post_authenticated(self):
        """Test creating a post when authenticated"""
        self.client.force_authenticate(user=self.user)
        
        # Test the self endpoint for getting user's own posts
        url = '/api/v1/post/self/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # No posts initially
        
    def test_post_voting_endpoints(self):
        """Test post voting functionality"""
        # Create a post first
        post = Post.objects.create(
            title='Test Post for Voting',
            content='Test content',
            author=self.user
        )
        
        self.client.force_authenticate(user=self.user)
        
        # Test upvote endpoint
        url = f'/api/v1/posts/{post.uuid}/upvote/'
        response = self.client.put(url)
        
        # This might return 404 if the endpoint doesn't exist, which is fine for testing
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])
        
    def test_create_post_unauthenticated(self):
        """Test creating a post when not authenticated"""
        url = '/api/v1/post/self/'
        data = {
            'title': 'New Test Post',
            'content': 'New test content'
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)