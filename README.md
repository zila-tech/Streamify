# Streamify

Streamify is a video streaming platform built with Django. It includes features such as user authentication, video navigation, video sharing, and an admin interface for uploading videos. The platform is designed to be responsive and visually appealing, with support for multiple themes and user customization.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Database Design](#database-design)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- User authentication (sign-up, log-in, email verification, password reset)
- Video navigation (next/previous video)
- Video sharing via email
- Admin interface for uploading videos
- Responsive design using Bootstrap 5
- Multiple themes with user customization
- Profile management (update profile, change password)
- Language support for multiple languages
- Custom video player with control box

## Technologies Used

- **Backend:** Django
- **Frontend:** Bootstrap 5, Font Awesome
- **Database:** SQLite (default), PostgreSQL (for Local), MYSql (for production)
- **Deployment:** PythonAnywhere
- **Version Control:** Git, GitHub

## Installation

### Prerequisites

- Python 3.10.12
- Django==5.0.6
- django_environ==0.11.2
- django-filter==24.2
- Git

### Clone the Repository

```bash
git clone https://github.com/zila-tech/Streamify.git
cd Streamify
```
                  

### Install Dependencies

- pip install -r requirements.txt

# Database Migration

- python manage.py makemigrations
- python manage.py migrate


### Create Superuser

- python manage.py createsuperuser

- Run the Development Server

- python manage.py runserver

### Usage

# User Authentication

- Sign up and log in to your account.
- Verify your email to activate your account.
- Reset your password if you forget it.

## Video Navigation

- Use the next and previous buttons to navigate through the videos.
- Video Sharing
- Share video links via email with your friends.


# Admin Interface

- Log in as an admin or staff to upload new videos and manage existing ones.

# Profile Management

- Update your profile information, change your password.

# Theme Customization

- Choose between light and dark themes.

# Database Design

- ER Diagram

# Contact
- Email: info.streamify.pvp@gmail.com
- GitHub: zila-tech