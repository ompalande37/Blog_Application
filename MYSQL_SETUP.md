# MySQL Setup Guide for Django Blog Application

This guide will help you set up MySQL database for your Django blog application.

## Prerequisites

1. **Python 3.8+** (already installed)
2. **MySQL Server** (needs to be installed)
3. **Git** (already installed)

## Step 1: Install MySQL Server

### Option A: Download MySQL Community Server
1. Go to https://dev.mysql.com/downloads/mysql/
2. Download MySQL Community Server for Windows
3. Run the installer and follow the setup wizard
4. Remember the root password you set during installation

### Option B: Using Chocolatey (if you have it)
```bash
choco install mysql
```

### Option C: Using XAMPP (includes MySQL, Apache, PHP)
1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP
3. Start MySQL service from XAMPP Control Panel

## Step 2: Verify MySQL Installation

Open Command Prompt or PowerShell and run:
```bash
mysql --version
```

You should see output like:
```
mysql  Ver 8.0.xx for Win64 on x86_64 (MySQL Community Server - GPL)
```

## Step 3: Start MySQL Service

### If using standalone MySQL:
```bash
net start mysql
```

### If using XAMPP:
1. Open XAMPP Control Panel
2. Click "Start" next to MySQL

## Step 4: Create Database

### Method 1: Using MySQL Command Line
```bash
mysql -u root -p
```

Enter your password when prompted, then run:
```sql
CREATE DATABASE django_blog_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### Method 2: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Run the SQL command above

## Step 5: Update Django Settings

Edit `django_blog/settings.py` and replace the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_blog_db',
        'USER': 'root',  # Change to your MySQL username
        'PASSWORD': 'your_password_here',  # Change to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

## Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 7: Create Superuser (if not already done)

```bash
python manage.py createsuperuser
```

## Step 8: Test the Application

```bash
python manage.py runserver
```

Visit http://localhost:8000 to see your blog!

## Troubleshooting

### Common Issues:

1. **"Access denied for user 'root'@'localhost'"**
   - Make sure you're using the correct password
   - Try creating a new MySQL user with proper permissions

2. **"Can't connect to MySQL server"**
   - Make sure MySQL service is running
   - Check if MySQL is running on the correct port (3306)

3. **"Unknown database 'django_blog_db'"**
   - Make sure you created the database in Step 4
   - Check the database name spelling

### Creating a New MySQL User (Recommended for Production)

```sql
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON django_blog_db.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
```

Then update your Django settings to use this user instead of root.

## Alternative: Continue with SQLite

If you prefer to continue with SQLite for development (which is already working), you can:

1. Keep the current SQLite configuration
2. The application will work perfectly for development
3. Switch to MySQL later when deploying to production

## Next Steps

After setting up MySQL:

1. **Start the server**: `python manage.py runserver`
2. **Visit the blog**: http://localhost:8000
3. **Access admin**: http://localhost:8000/admin/
4. **Create your first blog post**!

## API Testing

Once the server is running, you can test the API endpoints:

```bash
# Get JWT token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# List blog posts
curl http://localhost:8000/api/posts/
```

## Production Considerations

For production deployment:

1. **Use environment variables** for database credentials
2. **Create a dedicated MySQL user** (not root)
3. **Set up proper MySQL security**
4. **Configure MySQL for performance**
5. **Set up database backups**

## Support

If you encounter issues:

1. Check the MySQL error logs
2. Verify MySQL service is running
3. Test MySQL connection manually
4. Check Django settings for typos
5. Ensure all dependencies are installed 