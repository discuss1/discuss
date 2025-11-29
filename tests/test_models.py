"""
Basic model tests for the Reddit clone application
"""
from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post


class PostModelTest(TestCase):
    """Test cases for Post model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_post_creation(self):
        """Test creating a post"""
        post = Post.objects.create(
            title='Test Post',
            content='This is a test post content',
            author=self.user
        )
        
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post content')
        self.assertEqual(post.author, self.user)
        self.assertIsNotNone(post.uuid)
        self.assertIsNotNone(post.created_at)
        
    def test_post_str_method(self):
        """Test the string representation of a post"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        expected_str = f"Post: {post.uuid} published by {self.user.username}"
        self.assertEqual(str(post), expected_str)
        
    def test_post_score_calculation(self):
        """Test post score calculation"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        # Initially score should be 0
        self.assertEqual(post.score, 0)
        
    def test_post_status_default(self):
        """Test post status defaults to PUBLIC"""
        post = Post.objects.create(
            title='Test Post',
            content='Test content',
            author=self.user
        )
        
        self.assertEqual(post.status, Post.STATUS.PUBLIC)