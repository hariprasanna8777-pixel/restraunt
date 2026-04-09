# Deployment Guide

This guide covers deploying the Gourmet Restaurant application to various platforms.

## 🌐 Vercel Deployment (Recommended)

### Prerequisites
- GitHub account with the repository pushed
- Vercel account (free tier available)

### Steps

1. **Visit Vercel Dashboard**
   - Go to https://vercel.com/dashboard
   - Click "New Project"

2. **Import Repository**
   - Select "GitHub" as source
   - Find and select `restraunt` repository
   - Click "Import"

3. **Configure Project**
   - Framework: Other
   - Root Directory: ./
   - Build Command: (leave blank)
   - Output Directory: (leave blank)
   - Install Command: (leave blank)

4. **Set Environment Variables**
   - Click "Environment Variables"
   - Add the following:
     ```
     SECRET_KEY = your-secure-random-key
     FLASK_ENV = production
     ```
   - For production database (optional):
     ```
     DATABASE_URL = postgresql://user:pass@host/db
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at your custom domain

### Database Setup

**Option 1: SQLite (Default)**
- No additional setup needed
- Good for small to medium traffic
- Limited to single instance

**Option 2: PostgreSQL**
- Set `DATABASE_URL` in environment variables
- Recommended for production

### Monitoring

- View logs in Vercel dashboard
- Monitor performance metrics
- Set up alerts for errors

---

## 🐳 Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

ENV FLASK_APP=app_main.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app_main:app"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - ./:/app

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=restaurant
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Build and Run

```bash
docker-compose up -d
```

---

## 🚀 Linux Server Deployment (Ubuntu)

### Prerequisites
- Ubuntu 20.04+ VPS
- SSH access with sudo privileges
- Domain name (optional)

### Installation

1. **Update System**
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Install Dependencies**
```bash
sudo apt install -y python3 python3-pip python3-venv nginx
sudo apt install -y postgresql postgresql-contrib  # Optional
```

3. **Clone Repository**
```bash
cd /var/www
sudo git clone https://github.com/yourusername/restraunt.git
cd restraunt
```

4. **Create Virtual Environment**
```bash
python3 -m venv env
source env/bin/activate
pip install -r requirement.txt
pip install gunicorn
```

5. **Setup Database**
```bash
python3 -c "from app import create_app; app = create_app(); app.app_context().push()"
```

### Systemd Service Setup

Create `/etc/systemd/system/restaurant.service`:

```ini
[Unit]
Description=Gourmet Restaurant Application
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/restraunt
ExecStart=/var/www/restraunt/env/bin/gunicorn --workers 4 --bind 0.0.0.0:8000 app_main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable restaurant
sudo systemctl start restaurant
sudo systemctl status restaurant
```

### Nginx Configuration

Create `/etc/nginx/sites-available/restaurant`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
    }

    location /static {
        alias /var/www/restraunt/static;
        expires 30d;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/restaurant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL Setup (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🏠 Heroku Deployment

### Create Procfile
```
web: gunicorn app_main:app
```

### Add buildpacks
```bash
heroku buildpacks:add heroku/python
```

### Deploy
```bash
heroku login
git push heroku main
heroku run flask shell  # Create admin user if needed
```

---

## 📊 Production Checklist

- [ ] Set `SECRET_KEY` to a secure random value
- [ ] Set `FLASK_ENV=production`
- [ ] Configure external database (PostgreSQL recommended)
- [ ] Set up email service for notifications
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging
- [ ] Enable HTTPS/SSL certificate
- [ ] Configure firewall rules
- [ ] Set up automatic updates
- [ ] Create database backups
- [ ] Test disaster recovery
- [ ] Set up CDN for static files
- [ ] Configure rate limiting
- [ ] Enable security headers

---

## 🔒 Security Considerations

1. **Environment Variables**: Use `.env` file (gitignored)
2. **Database**: Use PostgreSQL with strong passwords
3. **SSL/TLS**: Always use HTTPS in production
4. **Updates**: Keep dependencies updated
5. **Backups**: Regular database backups
6. **Monitoring**: Set up error tracking and logging
7. **Rate Limiting**: Implement to prevent abuse
8. **CORS**: Configure appropriately

---

## 🆘 Troubleshooting

### App won't start
- Check logs: `heroku logs --tail`
- Verify dependencies: `pip check`
- Test locally first

### Database connection issues
- Verify DATABASE_URL format
- Check database credentials
- Ensure database server is running
- Check firewall rules

### Static files not loading
- Run: `python app_main.py --static`
- Configure CDN if needed

---

For more help, refer to Flask documentation: https://flask.palletsprojects.com/
