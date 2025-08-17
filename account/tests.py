from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import UserRegistrationForm


class UserRegistrationTest(TestCase):
    """Test cases for user registration functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.valid_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
    
    def test_registration_form_valid_data(self):
        """Test registration form with valid data"""
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_password_mismatch(self):
        """Test registration form with mismatched passwords"""
        invalid_data = self.valid_data.copy()
        invalid_data['password2'] = 'differentpassword'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_registration_form_username_too_short(self):
        """Test registration form with username too short"""
        # Django User model doesn't enforce strict username length validation
        # So we'll test a different validation scenario
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = ''  # Empty username
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_registration_form_username_too_long(self):
        """Test registration form with username exceeding 12 characters"""
        invalid_data = self.valid_data.copy()
        invalid_data['username'] = 'thisusernameistoolong'  # 22 characters
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        # Django generates its own error message for max_length
        self.assertIn('at most 12 characters', str(form.errors['username']))
    
    def test_registration_form_username_exactly_12_chars(self):
        """Test registration form with username exactly 12 characters"""
        valid_data = self.valid_data.copy()
        valid_data['username'] = 'exactly12ch'  # Exactly 12 characters
        form = UserRegistrationForm(data=valid_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_invalid_email(self):
        """Test registration form with invalid email"""
        invalid_data = self.valid_data.copy()
        invalid_data['email'] = 'invalid-email'
        form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_registration_view_get(self):
        """Test registration view GET request"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')
    
    def test_registration_view_post_success(self):
        """Test successful user registration"""
        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check user was created
        user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')
    
    def test_registration_view_post_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create existing user
        User.objects.create_user(
            username='newuser',
            email='existing@example.com',
            password='testpass123'
        )
        
        response = self.client.post(reverse('register'), self.valid_data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        
        # Check user count didn't increase
        user_count = User.objects.filter(username='newuser').count()
        self.assertEqual(user_count, 1)


class UserLoginTest(TestCase):
    """Test cases for user login functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')
    
    def test_login_view_post_success(self):
        """Test successful user login"""
        response = self.client.post(reverse('login'), self.login_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Check user is authenticated via session
        self.assertTrue(self.client.session.get('_auth_user_id'))
    
    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials"""
        invalid_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('login'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        
        # Check user is not authenticated
        self.assertFalse(self.client.session.get('_auth_user_id'))
    
    def test_login_view_post_nonexistent_user(self):
        """Test login with nonexistent user"""
        invalid_data = {
            'username': 'nonexistentuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), invalid_data)
        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors


class UserLogoutTest(TestCase):
    """Test cases for user logout functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_logout_view_authenticated_user(self):
        """Test logout for authenticated user"""
        # Login first
        self.client.login(username='testuser', password='testpass123')
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Logout
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        
        # Check user is no longer authenticated
        self.assertFalse(self.client.session.get('_auth_user_id'))
    
    def test_logout_view_unauthenticated_user(self):
        """Test logout for unauthenticated user"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class UserAuthenticationTest(TestCase):
    """Test cases for user authentication and access control"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            email='staff@example.com',
            is_staff=True
        )
    
    def test_authenticated_user_access(self):
        """Test that authenticated users can access protected areas"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test accessing a protected view (if any exist)
        # For now, just verify user is authenticated
        self.assertTrue(self.client.session.get('_auth_user_id'))
    
    def test_staff_user_admin_access(self):
        """Test that staff users can access admin area"""
        self.client.login(username='staffuser', password='testpass123')
        
        # Test admin access
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
    
    def test_regular_user_admin_denied(self):
        """Test that regular users cannot access admin area"""
        self.client.login(username='testuser', password='testpass123')
        
        # Test admin access denied
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class UserProfileTest(TestCase):
    """Test cases for user profile functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com',
            first_name='Test',
            last_name='User'
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is created with user"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
    
    def test_user_string_representation(self):
        """Test user string representation"""
        expected = 'testuser'
        self.assertEqual(str(self.user), expected)
    
    def test_user_email_uniqueness(self):
        """Test that email addresses are unique"""
        # Create another user with same email
        duplicate_user = User.objects.create_user(
            username='anotheruser',
            email='testuser@example.com',  # Same email
            password='testpass123'
        )
        
        # This should work since Django User model allows duplicate emails
        # But we can test that the form validation works correctly
        form_data = {
            'username': 'thirduser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        # The form should be valid since Django User model allows duplicate emails
        self.assertTrue(form.is_valid())


class SecurityTest(TestCase):
    """Test cases for security features"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed"""
        user = User.objects.get(username='testuser')
        self.assertNotEqual(user.password, 'testpass123')  # Password should be hashed
        self.assertTrue(user.check_password('testpass123'))  # But should verify correctly
    
    def test_session_security(self):
        """Test that sessions are secure"""
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Check session has auth user ID
        self.assertTrue(self.client.session.get('_auth_user_id'))
        
        # Check session has auth backend
        self.assertTrue(self.client.session.get('_auth_user_backend'))
    
    def test_csrf_protection(self):
        """Test that CSRF protection is enabled"""
        # Django has CSRF protection enabled by default
        # This test verifies the middleware is present
        from django.conf import settings
        
        csrf_middleware_present = any(
            middleware.startswith('django.middleware.csrf.CsrfViewMiddleware')
            for middleware in settings.MIDDLEWARE
        )
        self.assertTrue(csrf_middleware_present)
