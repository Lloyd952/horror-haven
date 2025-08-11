""" imports """
from django.conf import settings
from django.db import models
from django.db.models import Count, Avg
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """
    This creates a custom manager. It allows us to retrieve reviews using
    code like Review.published.all()
    Note: All models come with a default manager - the objects manager
    for example Review.objects.all()
    """

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status=Review.Status.PUBLISHED)

    def most_commented(self):
        return self.get_queryset().annotate(comment_count=Count(
            'comments')).order_by('-comment_count')[:3]

    def highest_rated(self):
        return self.get_queryset().annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:5]


class Review(models.Model):
    """ data model for a horror film review """
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    class Rating(models.IntegerChoices):
        ONE_STAR = 1, '⭐'
        TWO_STARS = 2, '⭐⭐'
        THREE_STARS = 3, '⭐⭐⭐'
        FOUR_STARS = 4, '⭐⭐⭐⭐'
        FIVE_STARS = 5, '⭐⭐⭐⭐⭐'

    title = models.CharField(max_length=200, help_text="Film title")
    slug = models.SlugField(
        max_length=210,
        unique_for_date='created_on'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='horror_reviews'
    )
    film_title = models.CharField(max_length=200, help_text="Original film title")
    year = models.IntegerField(help_text="Release year")
    director = models.CharField(max_length=200, help_text="Film director")
    rating = models.IntegerField(
        choices=Rating.choices,
        default=Rating.THREE_STARS,
        help_text="Your rating (1-5 stars)"
    )
    body = models.TextField(help_text="Your review")
    tags = TaggableManager(help_text="Tags like 'slasher', 'psychological', 'gore', etc.")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )
    # the default manager   ie Review.objects.all()
    objects = models.Manager()
    # our custom manager   ie Review.published.all()
    published = PublishedManager()

    class Meta:
        """
        This class defines the meta data for the model
        ordering is tell django that it should sort results by the updated_on
        field (latest first indicated by '-')
        indexes allows us to define the database indexing for this model
        """
        ordering = ['-updated_on']
        indexes = [
            models.Index(fields=['-updated_on']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f'{self.film_title} ({self.year}) - {self.get_rating_display()}'

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[
                self.created_on.year,
                self.created_on.month,
                self.created_on.day,
                self.slug
            ]
        )


class Comment(models.Model):

    post = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    body = models.TextField(max_length=800)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']
        indexes = [
            models.Index(fields=['created_on']),
        ]

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.film_title}'
