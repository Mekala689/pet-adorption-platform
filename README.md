# Pet Adoption Platform

A comprehensive web application built with Django and MongoDB for connecting pets in need with loving families.

## Features

### For Adopters
- Browse available pets with advanced filtering
- Save favorite pets
- Submit adoption applications
- Track application status
- User profile management

### For Shelters
- Add and manage pet listings
- Review adoption applications
- Schedule interviews with potential adopters
- Upload and manage documents
- Track adoption statistics

### For Administrators
- Manage users, pets, and applications
- View platform statistics
- Moderate content

## Technology Stack

- **Backend**: Django 4.2.7
- **Database**: MongoDB with Djongo
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **File Storage**: Local file system (configurable for cloud storage)
- **API**: Django REST Framework

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- MongoDB 4.0+ (optional, for production)

### Quick Setup (SQLite - Development)

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create a superuser**
   ```bash
   echo admin123 | python manage.py createsuperuser --username admin --email admin@example.com --noinput
   ```

4. **Populate sample data**
   ```bash
   python populate_sample_data.py
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser and go to `http://127.0.0.1:8000`

### Sample Login Credentials

After running the sample data script, you can use these credentials:

- **Admin**: username: `admin`, password: `admin123`
- **Shelter**: username: `happypaws_shelter`, password: `shelter123`
- **Adopter**: username: `john_doe`, password: `adopter123`

### Full Setup (MongoDB - Production)

1. **Install MongoDB dependencies**
   ```bash
   pip install djongo pymongo dnspython
   ```

2. **Update settings.py**
   Uncomment the MongoDB database configuration and comment out SQLite

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your MongoDB configuration
   ```

4. **Start MongoDB**
   Make sure MongoDB is running on your system.

5. **Follow steps 2-6 from Quick Setup**

## Project Structure

```
pet_adoption/
├── apps/
│   ├── core/           # Core functionality and home page
│   ├── users/          # User management and authentication
│   ├── pets/           # Pet listings and management
│   └── adoptions/      # Adoption applications and process
├── templates/          # HTML templates
├── static/            # CSS, JavaScript, and images
├── media/             # User-uploaded files
├── pet_adoption/      # Django project settings
└── manage.py          # Django management script
```

## Usage

### For Adopters

1. **Register an Account**
   - Visit the registration page
   - Choose "Adopter" as your user type
   - Complete your profile setup

2. **Browse Pets**
   - Use the search and filter options
   - View detailed pet information
   - Save pets to your favorites

3. **Apply for Adoption**
   - Click "Apply to Adopt" on a pet's detail page
   - Fill out the comprehensive application form
   - Submit and track your application status

### For Shelters

1. **Register as a Shelter**
   - Register with "Shelter" user type
   - Complete shelter profile with organization details
   - Wait for admin verification (if required)

2. **Add Pets**
   - Use the "Add Pet" feature
   - Upload photos and detailed information
   - Manage pet status (available, pending, adopted)

3. **Manage Applications**
   - Review incoming adoption applications
   - Schedule interviews with applicants
   - Approve or reject applications
   - Mark adoptions as completed

## API Endpoints

The platform includes a REST API for integration:

- `GET /api/stats/` - Platform statistics
- Additional endpoints available for pets, users, and applications

## Configuration

### Database Configuration

The application uses MongoDB through Djongo. Configure your database connection in the `.env` file:

```
DB_NAME=pet_adoption_db
DB_HOST=mongodb://localhost:27017
DB_USER=your_username
DB_PASSWORD=your_password
```

### Email Configuration

For email notifications (password reset, etc.), configure SMTP settings:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please contact [your-email@example.com] or create an issue in the repository.

## Future Enhancements

- Real-time messaging between adopters and shelters
- Integration with veterinary clinics
- Mobile application
- Advanced matching algorithms
- Payment processing for adoption fees
- Multi-language support
- Social media integration
