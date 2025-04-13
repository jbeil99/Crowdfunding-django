# Installation Guide

This guide will help you set up the Crowdfunding Django project on your local machine.

## Installation Steps

1. **Clone the Repository**
```bash
git clone <repository-url>
cd Crowdfunding-django
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# OR
.venv\Scripts\activate  # On Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up Environment Variables**
```bash
cp .env.example .env
```
Edit `.env` file and add your email configuration:
```
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_HOST_USER=your_email@gmail.com
```

5. **Create Required Directories**
```bash
mkdir -p media/images
```

6. **Add Default Images**
Place these default images in the media folder:
- `media/images/default_avatar.jpg` - Default user profile picture
- `media/images/default_thumbnail.jpg` - Default project thumbnail

7. **Run Migrations**
```bash
python manage.py migrate
```

8. **Create Admin and Staff Users**
```bash
python manage.py create_user
```
This will create:
- Staff user: staff@crowdfunding.com / Staff@123
- Admin user: admin@crowdfunding.com / Admin@123

9. **Seed Sample Data (Optional)**
```bash
python manage.py seed_data
```
This will create:
- 5 categories
- 10 projects (5 featured)
- Sample tags

10. **Run Development Server**
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

## API Documentation

- Main API documentation: [README.md](README.md)
- Authentication documentation: [AUTH.md](AUTH.md)




