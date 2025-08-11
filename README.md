# 🎬 Horror Haven - Horror Film Review Site

A Django-based horror film review website with a dark red theme and 5-star rating system.

## Features

- 🎭 Horror-themed design with blood red color scheme
- ⭐ 5-star rating system for horror films
- 📝 Detailed film reviews with director, year, and tags
- 💬 Comment system for user discussions
- 🏷️ Tag-based categorization (psychological, slasher, supernatural, etc.)
- 👤 User authentication and admin panel
- 📱 Responsive design

## Sample Reviews Included

- **The Shining (1980)** - Stanley Kubrick's psychological masterpiece
- **Hereditary (2018)** - Ari Aster's modern horror classic  
- **The Texas Chain Saw Massacre (1974)** - Tobe Hooper's revolutionary slasher

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run the server: `python manage.py runserver`
6. Visit: http://127.0.0.1:8000/

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed
- Git repository

### Deployment Steps

1. **Login to Heroku:**
   ```bash
   heroku login
   ```

2. **Create Heroku app:**
   ```bash
   heroku create your-horror-haven-app
   ```

3. **Add PostgreSQL database:**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. **Set environment variables:**
   ```bash
   heroku config:set SECRET_KEY="your-secret-key-here"
   heroku config:set DEBUG=False
   ```

5. **Deploy to Heroku:**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```

6. **Run migrations on Heroku:**
   ```bash
   heroku run python manage.py migrate
   ```

7. **Create superuser on Heroku:**
   ```bash
   heroku run python manage.py createsuperuser
   ```

8. **Open your app:**
   ```bash
   heroku open
   ```

### Environment Variables

Set these in Heroku:
- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Automatically set by Heroku PostgreSQL addon

## Admin Access

- URL: `/admin/`
- Use the superuser credentials you created

## Adding New Reviews

1. Login to admin panel
2. Go to "Reviews" section
3. Click "Add Review"
4. Fill in film details, rating, and review content
5. Add relevant tags
6. Set status to "Published"

## Technologies Used

- **Backend:** Django 5.0.7
- **Database:** PostgreSQL (Heroku) / SQLite (Development)
- **Static Files:** WhiteNoise
- **Server:** Gunicorn
- **Styling:** Custom CSS with horror theme
- **Tags:** django-taggit

## File Structure

```
├── blog/                 # Main app
│   ├── models.py        # Review and Comment models
│   ├── views.py         # View logic
│   ├── templates/       # HTML templates
│   └── static/css/      # Horror-themed CSS
├── account/             # User authentication
├── mysite/              # Project settings
├── requirements.txt     # Python dependencies
├── Procfile            # Heroku deployment
└── runtime.txt         # Python version
```

## Contributing

Feel free to submit issues and enhancement requests!

---

**🎭 Horror Haven - Where Fear Meets Film 🎭**
# horror-haven
