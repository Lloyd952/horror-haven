import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Review
from django.utils.text import slugify

# Get admin user
admin_user = User.objects.get(username='admin')

# Create sample reviews
reviews = [
    {
        'title': 'The Shining Review',
        'film_title': 'The Shining',
        'year': 1980,
        'director': 'Stanley Kubrick',
        'rating': Review.Rating.FIVE_STARS,
        'body': 'Stanley Kubrick\'s "The Shining" is a masterclass in psychological horror. Jack Nicholson delivers an iconic performance as Jack Torrance, a writer who descends into madness while caretaking the isolated Overlook Hotel. The film\'s ambiguity and atmospheric tension make it a timeless horror masterpiece.',
        'tags': ['psychological', 'supernatural', 'classic']
    },
    {
        'title': 'Hereditary Review',
        'film_title': 'Hereditary',
        'year': 2018,
        'director': 'Ari Aster',
        'rating': Review.Rating.FOUR_STARS,
        'body': 'Ari Aster\'s "Hereditary" redefines modern horror with its psychological depth and family trauma themes. Toni Collette\'s performance is devastating, and the film\'s exploration of grief and inherited mental illness creates genuine terror.',
        'tags': ['psychological', 'family', 'modern']
    },
    {
        'title': 'The Texas Chain Saw Massacre Review',
        'film_title': 'The Texas Chain Saw Massacre',
        'year': 1974,
        'director': 'Tobe Hooper',
        'rating': Review.Rating.FIVE_STARS,
        'body': 'Tobe Hooper\'s landmark film revolutionized horror cinema. Despite its title, it relies on atmosphere and psychological terror rather than gore. Leatherface remains one of cinema\'s most terrifying villains.',
        'tags': ['slasher', 'classic', 'cannibal']
    }
]

for review_data in reviews:
    slug = slugify(f"{review_data['film_title']}-{review_data['year']}")
    
    if not Review.objects.filter(slug=slug).exists():
        review = Review.objects.create(
            title=review_data['title'],
            film_title=review_data['film_title'],
            year=review_data['year'],
            director=review_data['director'],
            rating=review_data['rating'],
            body=review_data['body'],
            slug=slug,
            author=admin_user,
            status=Review.Status.PUBLISHED
        )
        
        for tag_name in review_data['tags']:
            review.tags.add(tag_name)
        
        print(f"Created: {review.film_title} ({review.year})")

print("Sample reviews created successfully!")
