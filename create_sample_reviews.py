#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Review
from django.utils.text import slugify
from datetime import datetime

def create_sample_reviews():
    # Get or create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@horrorhaven.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")
    
    # Sample horror film reviews
    reviews_data = [
        {
            'title': 'The Shining Review',
            'film_title': 'The Shining',
            'year': 1980,
            'director': 'Stanley Kubrick',
            'rating': Review.Rating.FIVE_STARS,
            'body': '''Stanley Kubrick's "The Shining" is a masterclass in psychological horror that continues to terrify audiences decades after its release. Based on Stephen King's novel, this film transcends the typical horror genre to become a deeply unsettling exploration of isolation, madness, and the supernatural.

Jack Nicholson delivers one of cinema's most iconic performances as Jack Torrance, a struggling writer who takes a job as the winter caretaker of the isolated Overlook Hotel. What begins as a peaceful retreat quickly descends into a nightmare as the hotel's dark history begins to manifest itself.

The film's brilliance lies in its ambiguity - is Jack truly possessed by the hotel's malevolent spirits, or is he simply losing his mind due to isolation and cabin fever? Kubrick masterfully keeps this question open, creating an atmosphere of constant unease.

The cinematography is nothing short of spectacular, with the hotel itself becoming a character through its labyrinthine corridors and haunting architecture. The use of Steadicam shots following Danny on his tricycle through the empty halls creates some of the most memorable and terrifying sequences in horror cinema.

"The Shining" is not just a horror film; it's a psychological thriller that explores themes of family dysfunction, addiction, and the fragility of the human psyche. The film's influence on the horror genre cannot be overstated, and it remains a benchmark for atmospheric horror storytelling.

Rating: 5/5 stars - A masterpiece of horror cinema that continues to haunt viewers with its psychological depth and technical brilliance.''',
            'tags': ['psychological', 'supernatural', 'classic', 'kubrick']
        },
        {
            'title': 'Hereditary Review',
            'film_title': 'Hereditary',
            'year': 2018,
            'director': 'Ari Aster',
            'rating': Review.Rating.FOUR_STARS,
            'body': '''Ari Aster's directorial debut "Hereditary" is a modern horror masterpiece that redefines what the genre is capable of achieving. This film is not just scary; it's deeply disturbing on a psychological level, exploring themes of grief, family trauma, and inherited mental illness.

Toni Collette delivers a tour-de-force performance as Annie Graham, a mother dealing with the death of her own mother while trying to hold her family together. The film's exploration of grief and its effects on family dynamics is both heartbreaking and terrifying.

What sets "Hereditary" apart from typical horror films is its commitment to character development and emotional realism. The horror doesn't come from cheap jump scares, but from the gradual unraveling of a family and the psychological torment they endure.

The film's third act is particularly effective, as it reveals the true nature of the supernatural elements at play. The final sequence is both visually stunning and emotionally devastating, leaving viewers with a sense of dread that lingers long after the credits roll.

"Hereditary" is a film that rewards multiple viewings, as its intricate plot and subtle foreshadowing become more apparent with each watch. It's a testament to Aster's skill as a filmmaker that he can create such a complex narrative while maintaining the film's emotional core.

Rating: 4/5 stars - A modern horror classic that proves the genre can be both terrifying and emotionally resonant.''',
            'tags': ['psychological', 'family', 'modern', 'aster']
        },
        {
            'title': 'The Texas Chain Saw Massacre Review',
            'film_title': 'The Texas Chain Saw Massacre',
            'year': 1974,
            'director': 'Tobe Hooper',
            'rating': Review.Rating.FIVE_STARS,
            'body': '''Tobe Hooper's "The Texas Chain Saw Massacre" is a landmark film that revolutionized the horror genre and established the template for the slasher film. Despite its title suggesting extreme violence, the film is surprisingly restrained in its gore, relying instead on atmosphere, sound design, and psychological terror.

The film follows a group of friends who encounter a family of cannibals in rural Texas, led by the iconic Leatherface. What makes this film so effective is its documentary-like approach to filmmaking, creating a sense of realism that makes the horror all the more believable.

The sound design is particularly noteworthy, with the constant whirring of the chainsaw creating an atmosphere of impending doom. The film's use of natural lighting and handheld camera work adds to its gritty, realistic feel.

Leatherface, played by Gunnar Hansen, is one of horror cinema's most terrifying villains. His animalistic behavior and the way he treats his victims like livestock creates a sense of primal fear that few other horror films have achieved.

"The Texas Chain Saw Massacre" is not just a horror film; it's a commentary on American society, exploring themes of family, isolation, and the breakdown of civilization. The film's influence on the horror genre is immeasurable, and it remains one of the most important horror films ever made.

Rating: 5/5 stars - A revolutionary horror film that continues to shock and terrify audiences with its raw intensity and social commentary.''',
            'tags': ['slasher', 'classic', 'cannibal', 'hooper']
        }
    ]
    
    created_count = 0
    for review_data in reviews_data:
        # Create slug from film title
        slug = slugify(f"{review_data['film_title']}-{review_data['year']}")
        
        # Check if review already exists
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
            
            # Add tags
            for tag_name in review_data['tags']:
                review.tags.add(tag_name)
            
            created_count += 1
            print(f"Created review: {review.film_title} ({review.year})")
        else:
            print(f"Review already exists: {review_data['film_title']} ({review_data['year']})")
    
    print(f"\nCreated {created_count} new horror film reviews!")
    print("You can now visit http://127.0.0.1:8000/blog/ to see your horror review site!")

if __name__ == '__main__':
    create_sample_reviews()
