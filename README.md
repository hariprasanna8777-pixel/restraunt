# 🍽️ Gourmet Restaurant - Production-Ready Web Application

A modern, full-featured restaurant management and ordering system built with Flask, featuring authentication, shopping cart, order management, and an admin panel.

## ✨ Features

### User Features
- **User Authentication**: Secure login/registration with password hashing
- **User Profiles**: Manage personal information and view order history
- **Shopping Cart**: Add items to cart and manage quantities
- **Order Management**: Place orders, track status, view order details
- **Table Reservations**: Book tables with date, time, and party size
- **Contact Form**: Send messages to restaurant management
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

### Admin Features
- **Admin Dashboard**: Real-time statistics and key metrics
- **Menu Management**: Add, edit, delete menu items
- **Order Management**: View all orders, update order status
- **Reservation Management**: Manage table reservations
- **User Management**: Control user access and admin privileges
- **Event Management**: Create and manage restaurant events
- **Message Management**: View and manage contact form submissions

### Technical Features
- **Modular Architecture**: Clean separation of concerns with blueprints
- **Database Models**: Comprehensive data models with relationships
- **Security**: Password hashing, CSRF protection, secure cookies
- **Modern UI**: Tailwind CSS for responsive, modern design
- **Form Validation**: WTForms with email and data validation
- **Production Ready**: Configured for Vercel deployments

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hariprasanna8777-pixel/restraunt.git
cd restraunt
```

2. **Create and activate virtual environment**
```bash
python -m venv env_new
source env_new/bin/activate  # On Windows: env_new\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirement.txt
```

4. **Run the application**
```bash
python app_main.py
```

The app will be available at `http://localhost:5000`

## 📁 Project Structure

```
restaurant/
├── app/                    # Main application package
│   ├── __init__.py        # App factory
│   ├── models.py          # Database models
│   ├── auth/              # Authentication blueprint
│   │   ├── forms.py       # WTForms for login/register
│   │   └── routes.py      # Auth routes
│   ├── main/              # Main app blueprint
│   │   └── routes.py      # Public routes (menu, orders, cart)
│   └── admin/             # Admin blueprint
│       └── routes.py      # Admin routes
├── templates/             # Jinja2 templates
│   ├── base.html         # Base template with navigation
│   ├── auth/             # Authentication templates
│   ├── admin/            # Admin templates
│   └── ...               # Other page templates
├── static/               # Static files (CSS, JS, images)
├── api/                  # Vercel serverless functions
├── config.py             # Application configuration
├── app_main.py           # Entry point for local development
├── vercel.json           # Vercel deployment config
└── requirement.txt       # Python dependencies
```

## 🗄️ Database Models

### User
- Store user authentication and profile information
- Relationships: Orders, Reservations

### MenuItem
- Menu items with category, price, and availability
- Relationships: OrderItems, CartItems

### Cart & CartItem
- Shopping cart management
- Track items, quantities, and subtotals

### Order & OrderItem
- Complete order tracking
- Status management (pending, confirmed, preparing, etc.)

### Reservation
- Table reservation system
- Date, time, party size, and notes

### ContactMessage
- Contact form submissions
- Track read/unread status

### Event
- Restaurant events and special occasions
- Date, location, capacity

## 🛡️ Security Features

- ✅ Password hashing with Werkzeug
- ✅ CSRF protection with Flask-WTF
- ✅ Secure session cookies (HTTPOnly, SameSite)
- ✅ User authentication with Flask-Login
- ✅ Admin-only routes with decorators
- ✅ Input validation on forms
- ✅ SQL injection prevention with SQLAlchemy ORM

## 🎨 UI/UX Features

- **Tailwind CSS**: Modern, responsive utility-first CSS framework
- **Mobile First**: Optimized for all device sizes
- **Interactive Elements**: Smooth hover effects and transitions
- **Font Awesome Icons**: Professional icon library
- **Gradient Design**: Modern gradient backgrounds
- **Dark Mode Ready**: Easily customizable color scheme

## 📦 Key Dependencies

- **Flask**: Web framework
- **SQLAlchemy**: ORM for database
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and CSRF protection
- **WTForms**: Form validation
- **Email-validator**: Email validation

## 🚀 Deployment

### Vercel Deployment

The app is configured for Vercel deployment:

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables:
   - `SECRET_KEY`: Your secret key for sessions
   - `DATABASE_URL`: PostgreSQL connection string (optional)
4. Deploy!

### Local Deployment

For production locally:

```bash
export FLASK_ENV=production
python app_main.py
```

## 👤 Demo Credentials

After first run, the app creates sample menu items. Create your admin account through the registration page and manually set `is_admin=True` in the database, or modify the sample data insertion.

## 📝 Usage Examples

### Customer Flow
1. **Register/Login** - Create account or sign in
2. **Browse Menu** - View available dishes
3. **Add to Cart** - Select items and quantities
4. **Checkout** - Enter delivery address
5. **Place Order** - Receive confirmation
6. **Track Order** - Monitor order status

### Admin Flow
1. **Login** - Admin credentials
2. **Dashboard** - View key metrics
3. **Manage Menu** - Add/edit/delete items
4. **Process Orders** - Update order status
5. **View Analytics** - Order and user statistics

## 🔧 Configuration

Edit `config.py` to customize:
- Database connection
- Session settings
- File upload limits
- Security settings

## 📞 Support

For issues or questions:
- Check GitHub Issues
- Review documentation
- Contact development team

## 📄 License

This project is licensed under the MIT License.

## 🙏 Credits

Built with modern web technologies and best practices for restaurant management systems.

---

**Version**: 2.0.0  
**Last Updated**: April 2024  
**Status**: Production Ready ✅
