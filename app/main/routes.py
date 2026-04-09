from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required
from app.models import db, MenuItem, Reservation, ContactMessage, Event, Cart, CartItem, Order, OrderItem

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Homepage"""
    featured_items = MenuItem.query.filter_by(is_available=True).limit(6).all()
    upcoming_events = Event.query.filter_by(is_active=True).limit(3).all()
    return render_template('index.html', featured_items=featured_items, events=upcoming_events)


@bp.route('/menu')
def menu():
    """Menu page with all items"""
    category = request.args.get('category', None)
    
    query = MenuItem.query.filter_by(is_available=True)
    if category:
        query = query.filter_by(category=category)
    
    items = query.all()
    categories = db.session.query(MenuItem.category).distinct().all()
    
    return render_template('menu.html', items=items, categories=[c[0] for c in categories])


@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@bp.route('/events')
def events():
    """Events page"""
    events = Event.query.filter_by(is_active=True).all()
    return render_template('events.html', events=events)


@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        if not (name and email and message):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('main.contact'))
        
        contact_msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(contact_msg)
        db.session.commit()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html')


@bp.route('/reservations', methods=['GET', 'POST'])
@login_required
def reservations():
    """Reservations page"""
    if request.method == 'POST':
        reservation_date = request.form.get('reservation_date', '').strip()
        reservation_time = request.form.get('reservation_time', '').strip()
        party_size = request.form.get('party_size', '').strip()
        notes = request.form.get('notes', '').strip() or None
        
        if not (reservation_date and reservation_time and party_size):
            flash('Please fill all required fields', 'danger')
            return redirect(url_for('main.reservations'))
        
        try:
            party_size = int(party_size)
            if party_size < 1 or party_size > 20:
                flash('Party size must be between 1 and 20', 'danger')
                return redirect(url_for('main.reservations'))
        except ValueError:
            flash('Invalid party size', 'danger')
            return redirect(url_for('main.reservations'))
        
        reservation = Reservation(
            user_id=current_user.id,
            reservation_date=reservation_date,
            reservation_time=reservation_time,
            party_size=party_size,
            notes=notes
        )
        db.session.add(reservation)
        db.session.commit()
        
        flash('Reservation created successfully! We will confirm shortly.', 'success')
        return redirect(url_for('main.reservations'))
    
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('reservations.html', reservations=user_reservations)


@bp.route('/cart')
@login_required
def view_cart():
    """View shopping cart"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        flash('Your cart is empty', 'info')
        return render_template('cart.html', cart=None)
    
    return render_template('cart.html', cart=cart)


@bp.route('/api/cart/add', methods=['POST'])
@login_required
def add_to_cart():
    """API endpoint to add item to cart"""
    data = request.get_json()
    menu_item_id = data.get('menu_item_id')
    quantity = data.get('quantity', 1)
    
    menu_item = MenuItem.query.get_or_404(menu_item_id)
    
    if not menu_item.is_available:
        return jsonify({'error': 'Item not available'}), 400
    
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, menu_item_id=menu_item_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, menu_item_id=menu_item_id, quantity=quantity)
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'success': True, 'total': cart.total})


@bp.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    """API endpoint to remove item from cart"""
    cart = Cart.query.filter_by(user_id=current_user.id).first_or_404()
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first_or_404()
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'success': True, 'total': cart.total})


@bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    
    if not cart or not cart.items:
        flash('Your cart is empty', 'danger')
        return redirect(url_for('main.view_cart'))
    
    if request.method == 'POST':
        delivery_address = request.form.get('delivery_address', '').strip()
        instructions = request.form.get('instructions', '').strip() or None
        
        if not delivery_address:
            flash('Please enter a delivery address', 'danger')
            return redirect(url_for('main.checkout'))
        
        # Create order from cart
        order = Order(
            user_id=current_user.id,
            total_amount=cart.total,
            delivery_address=delivery_address,
            instructions=instructions
        )
        
        # Add order items
        for cart_item in cart.items:
            order_item = OrderItem(
                menu_item_id=cart_item.menu_item_id,
                quantity=cart_item.quantity,
                price=cart_item.menu_item.price
            )
            order.items.append(order_item)
        
        db.session.add(order)
        
        # Clear cart
        for item in cart.items:
            db.session.delete(item)
        
        db.session.commit()
        
        flash('Order placed successfully! You can track it on the orders page.', 'success')
        return redirect(url_for('main.orders'))
    
    return render_template('checkout.html', cart=cart)


@bp.route('/orders')
@login_required
def orders():
    """View user orders"""
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)


@bp.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    """View order details"""
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_detail.html', order=order)
