from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models import db, User, MenuItem
from app.auth import bp as auth_bp
from app.main import bp as main_bp
from app.admin import bp as admin_bp
from config import Config

migrate = Migrate()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    """Load user by ID"""
    return User.query.get(int(id))


def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        _insert_sample_data()
    
    return app


def _insert_sample_data():
    """Insert sample data if database is empty"""
    if MenuItem.query.first() is not None:
        return  # Data already exists
    
    sample_items = [
        MenuItem(name="Margherita Pizza", description="Fresh mozzarella, basil, tomato sauce", 
                price=299, category="Pizza", is_available=True),
        MenuItem(name="Caesar Salad", description="Crisp romaine, parmesan, croutons, caesar dressing", 
                price=199, category="Salads", is_available=True),
        MenuItem(name="Grilled Salmon", description="Atlantic salmon, lemon butter, seasonal veg", 
                price=499, category="Mains", is_available=True),
        MenuItem(name="Tom Yum Soup", description="Thai red curry, shrimp, mushrooms, lime", 
                price=149, category="Soups", is_available=True),
        MenuItem(name="Paneer Tikka", description="House spiced paneer, mint chutney", 
                price=279, category="Appetizers", is_available=True),
        MenuItem(name="Chocolate Lava Cake", description="Warm chocolate cake with molten center", 
                price=179, category="Desserts", is_available=True),
        MenuItem(name="Burger Deluxe", description="Beef patty, cheddar, lettuce, tomato, special sauce", 
                price=349, category="Burgers", is_available=True),
        MenuItem(name="Vegetable Biryani", description="Basmati rice, mixed vegetables, aromatic spices", 
                price=229, category="Rice Dishes", is_available=True),
    ]
    
    for item in sample_items:
        db.session.add(item)
    
    db.session.commit()
