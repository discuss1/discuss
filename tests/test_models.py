"""
Basic model tests for the Reddit clone application
"""
from django.test import TestCase
from django.contrib.auth.models import User
from apps.posts.models import Post
from apps.groups.models import Group


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
        
        self.assertEqual(str(post), 'Test Post')


class GroupModelTest(TestCase):
    """Test cases for Group model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_group_creation(self):
        """Test creating a group"""
        group = Group.objects.create(
            name='testgroup',
            description='A test group',
            created_by=self.user
        )
        
        self.assertEqual(group.name, 'testgroup')
        self.assertEqual(group.description, 'A test group')
        self.assertEqual(group.created_by, self.user)
        self.assertIsNotNone(group.uuid)
        
    def test_group_str_method(self):
        """Test the string representation of a group"""
        group = Group.objects.create(
            name='testgroup',
            description='Test description',
            created_by=self.user
        )
        
        self.assertEqual(str(group), 'testgroup')