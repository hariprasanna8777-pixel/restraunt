from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import db, User, MenuItem, Order, Reservation, ContactMessage, Event, OrderItem

bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard"""
    # Statistics
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.created_at >= datetime.utcnow() - timedelta(days=30)
    ).scalar() or 0
    pending_orders = Order.query.filter_by(status='pending').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Orders by status
    orders_by_status = db.session.query(
        Order.status, 
        func.count(Order.id)
    ).group_by(Order.status).all()
    
    return render_template('admin/dashboard.html',
                         total_orders=total_orders,
                         total_users=total_users,
                         total_revenue=total_revenue,
                         pending_orders=pending_orders,
                         recent_orders=recent_orders,
                         orders_by_status=orders_by_status)


@bp.route('/menu-items')
@admin_required
def menu_items():
    """Manage menu items"""
    page = request.args.get('page', 1, type=int)
    items = MenuItem.query.paginate(page=page, per_page=20)
    return render_template('admin/menu_items.html', items=items)


@bp.route('/menu-items/new', methods=['GET', 'POST'])
@admin_required
def new_menu_item():
    """Create new menu item"""
    if request.method == 'POST':
        item = MenuItem(
            name=request.form.get('name'),
            description=request.form.get('description'),
            price=float(request.form.get('price')),
            category=request.form.get('category'),
            image_url=request.form.get('image_url'),
            is_available=request.form.get('is_available') == 'on'
        )
        db.session.add(item)
        db.session.commit()
        flash('Menu item created successfully', 'success')
        return redirect(url_for('admin.menu_items'))
    
    return render_template('admin/edit_menu_item.html', item=None)


@bp.route('/menu-items/<int:item_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_menu_item(item_id):
    """Edit menu item"""
    item = MenuItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))
        item.category = request.form.get('category')
        item.image_url = request.form.get('image_url')
        item.is_available = request.form.get('is_available') == 'on'
        db.session.commit()
        flash('Menu item updated successfully', 'success')
        return redirect(url_for('admin.menu_items'))
    
    return render_template('admin/edit_menu_item.html', item=item)


@bp.route('/menu-items/<int:item_id>/delete', methods=['POST'])
@admin_required
def delete_menu_item(item_id):
    """Delete menu item"""
    item = MenuItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item deleted successfully', 'success')
    return redirect(url_for('admin.menu_items'))


@bp.route('/orders')
@admin_required
def orders():
    """Manage all orders"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', None)
    
    query = Order.query
    if status:
        query = query.filter_by(status=status)
    
    orders = query.order_by(Order.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/orders.html', orders=orders, current_status=status)


@bp.route('/orders/<int:order_id>/update-status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']:
        order.status = new_status
        db.session.commit()
        flash(f'Order status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.orders'))


@bp.route('/reservations')
@admin_required
def reservations():
    """Manage all reservations"""
    page = request.args.get('page', 1, type=int)
    reservations = Reservation.query.order_by(Reservation.reservation_date.desc()).paginate(page=page, per_page=20)
    return render_template('admin/reservations.html', reservations=reservations)


@bp.route('/reservations/<int:reservation_id>/update-status', methods=['POST'])
@admin_required
def update_reservation_status(reservation_id):
    """Update reservation status"""
    reservation = Reservation.query.get_or_404(reservation_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'confirmed', 'cancelled', 'completed']:
        reservation.status = new_status
        db.session.commit()
        flash(f'Reservation status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin.reservations'))


@bp.route('/messages')
@admin_required
def messages():
    """View contact messages"""
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('admin/messages.html', messages=messages)


@bp.route('/messages/<int:message_id>/mark-read', methods=['POST'])
@admin_required
def mark_message_read(message_id):
    """Mark message as read"""
    message = ContactMessage.query.get_or_404(message_id)
    message.is_read = True
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/events')
@admin_required
def events():
    """Manage events"""
    page = request.args.get('page', 1, type=int)
    events = Event.query.paginate(page=page, per_page=20)
    return render_template('admin/events.html', events=events)


@bp.route('/events/new', methods=['GET', 'POST'])
@admin_required
def new_event():
    """Create new event"""
    if request.method == 'POST':
        event = Event(
            title=request.form.get('title'),
            description=request.form.get('description'),
            event_date=datetime.fromisoformat(request.form.get('event_date')),
            location=request.form.get('location'),
            image_url=request.form.get('image_url'),
            capacity=int(request.form.get('capacity')) if request.form.get('capacity') else None,
            is_active=request.form.get('is_active') == 'on'
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/edit_event.html', event=None)


@bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_event(event_id):
    """Edit event"""
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.event_date = datetime.fromisoformat(request.form.get('event_date'))
        event.location = request.form.get('location')
        event.image_url = request.form.get('image_url')
        event.capacity = int(request.form.get('capacity')) if request.form.get('capacity') else None
        event.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash('Event updated successfully', 'success')
        return redirect(url_for('admin.events'))
    
    return render_template('admin/edit_event.html', event=event)


@bp.route('/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def delete_event(event_id):
    """Delete event"""
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully', 'success')
    return redirect(url_for('admin.events'))


@bp.route('/users')
@admin_required
def users():
    """Manage users"""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20)
    return render_template('admin/users.html', users=users)


@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    """Toggle user admin status"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot change your own admin status', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'User {user.username} admin status updated', 'success')
    return redirect(url_for('admin.users'))
