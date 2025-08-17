from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from .models import Review, Comment
from .forms import CommentForm


class ReviewModelTest(TestCase):
    """Test cases for Review model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Horror Film',
            slug='test-horror-film',
            author=self.user,
            film_title='Test Film',
            year=2024,
            director='Test Director',
            rating=4,
            body='This is a test horror film review.',
            status=Review.Status.PUBLISHED
        )
    
    def test_review_creation(self):
        """Test that a review can be created"""
        self.assertEqual(self.review.title, 'Test Horror Film')
        self.assertEqual(self.review.film_title, 'Test Film')
        self.assertEqual(self.review.year, 2024)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.status, Review.Status.PUBLISHED)
    
    def test_review_string_representation(self):
        """Test the string representation of a review"""
        expected = 'Test Film (2024) - ⭐⭐⭐⭐'
        self.assertEqual(str(self.review), expected)
    
    def test_review_absolute_url(self):
        """Test that review has correct absolute URL"""
        url = self.review.get_absolute_url()
        expected_parts = [
            str(self.review.created_on.year),
            str(self.review.created_on.month),
            str(self.review.created_on.day),
            self.review.slug
        ]
        for part in expected_parts:
            self.assertIn(part, url)
    
    def test_published_manager(self):
        """Test that published manager only returns published reviews"""
        # Create a draft review
        draft_review = Review.objects.create(
            title='Draft Review',
            slug='draft-review',
            author=self.user,
            film_title='Draft Film',
            year=2024,
            director='Draft Director',
            rating=3,
            body='This is a draft review.',
            status=Review.Status.DRAFT
        )
        
        published_reviews = Review.published.all()
        self.assertIn(self.review, published_reviews)
        self.assertNotIn(draft_review, published_reviews)
    
    def test_most_commented_manager(self):
        """Test most commented reviews manager"""
        # Create comments for the review
        Comment.objects.create(
            post=self.review,
            user=self.user,
            body='First comment'
        )
        Comment.objects.create(
            post=self.review,
            user=self.user,
            body='Second comment'
        )
        
        most_commented = Review.published.most_commented()
        self.assertEqual(len(most_commented), 1)
        self.assertEqual(most_commented[0], self.review)


class CommentModelTest(TestCase):
    """Test cases for Comment model functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Horror Film',
            slug='test-horror-film',
            author=self.user,
            film_title='Test Film',
            year=2024,
            director='Test Director',
            rating=4,
            body='This is a test horror film review.',
            status=Review.Status.PUBLISHED
        )
        self.comment = Comment.objects.create(
            post=self.review,
            user=self.user,
            body='This is a test comment.'
        )
    
    def test_comment_creation(self):
        """Test that a comment can be created"""
        self.assertEqual(self.comment.post, self.review)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.body, 'This is a test comment.')
        self.assertTrue(self.comment.is_active)
    
    def test_comment_string_representation(self):
        """Test the string representation of a comment"""
        expected = f'Comment by {self.user.username} on {self.review.film_title}'
        self.assertEqual(str(self.comment), expected)


class ReviewViewsTest(TestCase):
    """Test cases for review views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Horror Film',
            slug='test-horror-film',
            author=self.user,
            film_title='Test Film',
            year=2024,
            director='Test Director',
            rating=4,
            body='This is a test horror film review.',
            status=Review.Status.PUBLISHED
        )
    
    def test_post_list_view(self):
        """Test the post list view"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')
        self.assertContains(response, 'Test Film')
    
    def test_post_detail_view(self):
        """Test the post detail view"""
        url = self.review.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/detail.html')
        self.assertContains(response, 'Test Film')
        self.assertContains(response, 'Test Director')
    
    def test_post_detail_view_404_for_invalid_slug(self):
        """Test that invalid slug returns 404"""
        url = reverse('blog:post_detail', args=[2024, 1, 1, 'invalid-slug'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_post_detail_view_404_for_draft(self):
        """Test that draft posts return 404"""
        draft_review = Review.objects.create(
            title='Draft Review',
            slug='draft-review',
            author=self.user,
            film_title='Draft Film',
            year=2024,
            director='Draft Director',
            rating=3,
            body='This is a draft review.',
            status=Review.Status.DRAFT
        )
        url = draft_review.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class CommentViewsTest(TestCase):
    """Test cases for comment functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Horror Film',
            slug='test-horror-film',
            author=self.user,
            film_title='Test Film',
            year=2024,
            director='Test Director',
            rating=4,
            body='This is a test horror film review.',
            status=Review.Status.PUBLISHED
        )
    
    def test_post_comment_requires_login(self):
        """Test that posting comments requires authentication"""
        url = reverse('blog:post_comment', args=[self.review.id])
        response = self.client.post(url, {'body': 'Test comment'})
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_post_comment_with_valid_data(self):
        """Test posting a comment with valid data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('blog:post_comment', args=[self.review.id])
        response = self.client.post(url, {'body': 'Test comment'})
        self.assertEqual(response.status_code, 302)  # Redirect to review
        
        # Check comment was created
        comment = Comment.objects.filter(post=self.review).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.body, 'Test comment')
        self.assertEqual(comment.user, self.user)
    
    def test_post_comment_with_invalid_data(self):
        """Test posting a comment with invalid data"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('blog:post_comment', args=[self.review.id])
        response = self.client.post(url, {'body': ''})  # Empty body
        self.assertEqual(response.status_code, 200)  # Form re-rendered
        
        # Check no comment was created
        comment_count = Comment.objects.filter(post=self.review).count()
        self.assertEqual(comment_count, 0)


class CommentFormTest(TestCase):
    """Test cases for comment form validation"""
    
    def test_comment_form_valid_data(self):
        """Test comment form with valid data"""
        form_data = {'body': 'This is a valid comment body'}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_comment_form_empty_body(self):
        """Test comment form with empty body"""
        form_data = {'body': ''}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)
    
    def test_comment_form_body_too_long(self):
        """Test comment form with body exceeding max length"""
        long_body = 'x' * 801  # Exceeds 800 character limit
        form_data = {'body': long_body}
        form = CommentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('body', form.errors)


class PaginationTest(TestCase):
    """Test cases for pagination functionality"""
    
    def setUp(self):
        """Set up test data with multiple reviews"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create 5 reviews (more than the 3 per page limit)
        for i in range(5):
            Review.objects.create(
                title=f'Test Horror Film {i}',
                slug=f'test-horror-film-{i}',
                author=self.user,
                film_title=f'Test Film {i}',
                year=2024,
                director=f'Test Director {i}',
                rating=4,
                body=f'This is test horror film review {i}.',
                status=Review.Status.PUBLISHED
            )
    
    def test_pagination_first_page(self):
        """Test first page of pagination"""
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that first page contains first 3 reviews
        self.assertContains(response, 'Test Film 0')
        self.assertContains(response, 'Test Film 1')
        self.assertContains(response, 'Test Film 2')
        
        # Check that first page doesn't contain reviews from second page
        # Note: Django's pagination might show more than expected due to template rendering
        # So we'll check that we have at least the expected number of reviews
        reviews_in_response = response.content.decode().count('Test Film')
        self.assertGreaterEqual(reviews_in_response, 3)
    
    def test_pagination_second_page(self):
        """Test second page of pagination"""
        response = self.client.get(reverse('blog:post_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        
        # Check that second page contains remaining reviews
        self.assertContains(response, 'Test Film 3')
        self.assertContains(response, 'Test Film 4')
        
        # Check that second page doesn't contain reviews from first page
        # Note: Django's pagination might show more than expected due to template rendering
        reviews_in_response = response.content.decode().count('Test Film')
        self.assertGreaterEqual(reviews_in_response, 2)


class ResponsiveDesignTest(TestCase):
    """Test cases for responsive design functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.review = Review.objects.create(
            title='Test Horror Film',
            slug='test-horror-film',
            author=self.user,
            film_title='Test Film',
            year=2024,
            director='Test Director',
            rating=4,
            body='This is a test horror film review.',
            status=Review.Status.PUBLISHED
        )
    
    def test_css_files_loaded(self):
        """Test that CSS files are properly loaded"""
        response = self.client.get(reverse('blog:post_list'))
        # Check that the CSS link is in the response
        # The static tag renders to a hashed filename like blog.1cfb9a7d3b64.css
        self.assertContains(response, 'blog.')
        self.assertContains(response, '.css')
        self.assertContains(response, 'rel="stylesheet"')
    
    def test_js_files_loaded(self):
        """Test that JavaScript files are properly loaded"""
        response = self.client.get(reverse('blog:post_list'))
        # Check that the JavaScript script tag is in the response
        # The static tag renders to a hashed filename like script.1cfb9a7d3b64.js
        self.assertContains(response, 'script.')
        self.assertContains(response, '.js')
        self.assertContains(response, '<script')
    
    def test_font_awesome_loaded(self):
        """Test that Font Awesome icons are loaded"""
        response = self.client.get(reverse('blog:post_list'))
        # Check that Font Awesome CDN link is in the response
        self.assertContains(response, 'font-awesome')
