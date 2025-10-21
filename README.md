# Novel Net - Your Literary Journey Starts Here

A comprehensive Django-based book review and recommendation platform that allows users to discover, share, and discuss books with a community of book lovers.

## Features

- **Book Discovery**: Browse and search through a vast collection of books
- **Personal Libraries**: Create and manage your own book collections with custom shelves
- **Reviews & Ratings**: Share your thoughts and read reviews from other users
- **Book Clubs**: Join or create book clubs to discuss your favorite reads
- **User Uploads**: Upload and share your own books with the community
- **Download Books**: Access books uploaded by other users
- **Social Features**: Connect with fellow book enthusiasts

## Technology Stack

- **Backend**: Django 4.2+ with Python 3.10+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in user authentication
- **File Handling**: Django's file upload and media handling
- **API Integration**: Google Books API for external book data

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone
   cd novel-net
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   **Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **Mac/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

### Quick Start Scripts

For Windows users, use `start_project.bat`:
```bash
start_project.bat
```

For Mac/Linux users, use `start_project.sh`:
```bash
chmod +x start_project.sh
./start_project.sh
```

## Project Structure

```
novel-net/
├── novelnet/                # Django project settings
├── books/                   # Books app (models, views, forms)
├── reviews/                 # Reviews app
├── clubs/                   # Book clubs app
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploaded files
├── requirements.txt         # Python dependencies
├── manage.py                # Django management script
├── Procfile                 # Deployment configuration
├── runtime.txt              # Python version specification
└── README.md               # This file
```

## Key Features

### Book Management
- Upload books in various formats (PDF, EPUB, MOBI, TXT)
- Add book covers and metadata
- Set books as public or private
- Track download statistics

### User Experience
- Responsive design that works on all devices
- Intuitive navigation and user interface
- Real-time search and filtering
- Social features for book discovery

### Community Features
- Join book clubs based on your interests
- Participate in discussions about books
- Share reviews and recommendations
- Connect with like-minded readers

## Deployment

The project is configured for easy deployment on platforms like:
- **Railway**: Use the provided `Procfile` and `runtime.txt`
- **Heroku**: Compatible with Heroku's Django deployment
- **DigitalOcean**: Can be deployed on DigitalOcean App Platform
- **AWS**: Compatible with AWS Elastic Beanstalk

### Environment Variables

For production deployment, set these environment variables:
- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain(s)
- `DATABASE_URL`: Database connection string (for PostgreSQL)
- `GOOGLE_BOOKS_API_KEY`: Your Google Books API key

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please:
1. Check the existing issues on GitHub
2. Create a new issue with detailed information
3. Contact the development team

---

**Novel Net** - Connecting readers, one book at a time. 📚
