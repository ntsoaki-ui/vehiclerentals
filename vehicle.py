import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Flask app
app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'vehicle-rental-secret-key-2024')

# SQLite database path
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vehicle_rental.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Create database if it doesn't exist (important for Render)
if not os.path.exists(db_path):
    db.create_all()

# Example route
@app.route('/')
def home():
    return "Vehicle Rental System is running!"

# Ensure Gunicorn sees 'app'
if __name__ == '__main__':
    app.run(debug=True)
# Sesotho names for random generation
SESOTHO_FIRST_NAMES = [
    'Thabo', 'Palesa', 'Lerato', 'Tumelo', 'Mpho', 'Khotso', 'Nthabiseng', 'Matshidiso',
    'Refilwe', 'Kabelo', 'Mosiuoa', 'Masechaba', 'Sello', 'Mamello', 'Tshepo', 'Bonolo',
    'Kedibone', 'Teboho', 'Mantšebo', 'Moleboheng', 'Mohlomi', 'Malebohang', 'Mphatšo',
    'Lisebo', 'Tšepang', 'Mamokete', 'Mampho', 'Ntšeliseng', 'Mampoi', 'Mamokhosi',
    'Lerato', 'Mpho', 'Thabiso', 'Relebohile', 'Nthati', 'Manko', 'Mphatšo', 'Lehlohonolo',
    'Molefi', 'Puleng', 'Mosa', 'Tšepiso', 'Mokhali', 'Moleboheng', 'Manko', 'Mpho',
    'Lerato', 'Thabo', 'Palesa', 'Khotso', 'Tumelo', 'Nthabiseng', 'Refilwe', 'Kabelo'
]

SESOTHO_LAST_NAMES = [
    'Mokoena', 'Moloi', 'Motaung', 'Nkosi', 'Khanye', 'Mofokeng', 'Mohlomi', 'Phiri',
    'Sello', 'Thamae', 'Motsamai', 'Mohlaloga', 'Mokhethi', 'Mohlomi', 'Mohlaloga',
    'Mokone', 'Mphahlele', 'Mothapo', 'Mohlomi', 'Mohlaloga', 'Mokitimi', 'Mohlomi',
    'Mohlaloga', 'Mokone', 'Mphahlele', 'Mothapo', 'Mohlomi', 'Mohlaloga', 'Mokitimi',
    'Lereko', 'Mofokeng', 'Mokoena', 'Mothapo', 'Nkosi', 'Phiri', 'Sello', 'Thamae',
    'Motsamai', 'Mohlomi', 'Mokhethi', 'Mohlaloga', 'Mokone', 'Mphahlele', 'Mokitimi',
    'Mohlomi', 'Mohlaloga', 'Mokone', 'Mphahlele', 'Mothapo', 'Mohlomi', 'Mohlaloga',
    'Mokitimi', 'Lereko', 'Mofokeng', 'Mokoena', 'Mothapo', 'Nkosi', 'Phiri'
]

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='employee')
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    id_number = db.Column(db.String(50))
    license_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Active')

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.String(20), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(30))
    plate_number = db.Column(db.String(20), unique=True, nullable=False)
    daily_rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Available')
    mileage = db.Column(db.Float, default=0)
    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))
    seats = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rental_id = db.Column(db.String(20), unique=True, nullable=False)
    customer_id = db.Column(db.String(20), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    vehicle_id = db.Column(db.String(20), nullable=False)
    vehicle_info = db.Column(db.String(200), nullable=False)
    rental_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    actual_return_date = db.Column(db.Date)
    daily_rate = db.Column(db.Float, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    deposit = db.Column(db.Float, default=0)
    payment_status = db.Column(db.String(20), default='Pending')
    rental_status = db.Column(db.String(20), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(20), unique=True, nullable=False)
    rental_id = db.Column(db.String(20), nullable=False)
    customer_id = db.Column(db.String(20), nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20), default='Completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), default='Vehicle Rental System')
    deposit_rate = db.Column(db.Float, default=20.0)
    late_fee_per_day = db.Column(db.Float, default=50.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_database():
    """Initialize the database with default data if tables are empty"""
    print("Initializing database...")
    
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # Create default admin user with Sesotho name
            admin = User(
                username='admin',
                email='admin@vehiclerental.com',
                full_name='Mpho Lereko',
                role='admin',
                phone='+266 500-1234'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Created admin user: Mpho Lereko")
        
        # Check if settings exist
        settings = SystemSettings.query.first()
        if not settings:
            settings = SystemSettings()
            db.session.add(settings)
            print("Created system settings")
        
        # Check if vehicles exist
        vehicle_count = Vehicle.query.count()
        if vehicle_count == 0:
            # Add 5 default vehicles
            vehicles = [
                ('V001', 'Toyota', 'Corolla', 2022, 'White', 'ABC123', 1500.00, 'Available', 'Petrol', 'Automatic', 5),
                ('V002', 'Honda', 'CR-V', 2021, 'Black', 'DEF456', 2000.00, 'Available', 'Petrol', 'Automatic', 7),
                ('V003', 'Ford', 'Ranger', 2023, 'Blue', 'GHI789', 2500.00, 'Available', 'Diesel', 'Manual', 5),
                ('V004', 'Mercedes', 'C-Class', 2022, 'Silver', 'JKL012', 3500.00, 'Maintenance', 'Petrol', 'Automatic', 5),
                ('V005', 'Nissan', 'X-Trail', 2021, 'Red', 'MNO345', 1800.00, 'Available', 'Petrol', 'Automatic', 5)
            ]
            
            for vehicle_data in vehicles:
                vehicle = Vehicle(
                    vehicle_id=vehicle_data[0],
                    make=vehicle_data[1],
                    model=vehicle_data[2],
                    year=vehicle_data[3],
                    color=vehicle_data[4],
                    plate_number=vehicle_data[5],
                    daily_rate=vehicle_data[6],
                    status=vehicle_data[7],
                    fuel_type=vehicle_data[8],
                    transmission=vehicle_data[9],
                    seats=vehicle_data[10]
                )
                db.session.add(vehicle)
            print(f"Added {len(vehicles)} default vehicles")
        
        # Check if customers exist
        customer_count = Customer.query.count()
        if customer_count == 0:
            # Add 6 default customers with SPECIFIC Sesotho names
            customers = [
                ('C001', 'Mpho Lereko', 'mpho.lereko@email.com', '+266 501-2345', 
                 '123 Maluti Street Maseru 100', 'ID79012345', 'LIC0012345'),
                
                ('C002', 'Thabo Mokoena', 'thabo.mokoena@email.com', '+266 502-3456', 
                 '456 Thaba Bosiu Road Roma 180', 'ID79123456', 'LIC0023456'),
                
                ('C003', 'Palesa Moloi', 'palesa.moloi@email.com', '+266 503-4567', 
                 '789 Mountain View Teyateyaneng 200', 'ID79234567', 'LIC0034567'),
                
                ('C004', 'Lerato Motaung', 'lerato.motaung@email.com', '+266 504-5678', 
                 '321 River Side Maputsoe 300', 'ID79345678', 'LIC0045678'),
                
                ('C005', 'Tumelo Nkosi', 'tumelo.nkosi@email.com', '+266 505-6789', 
                 '654 Sunset Blvd Mohale\'s Hoek 400', 'ID79456789', 'LIC0056789'),
                
                ('C006', 'Teboho Mohlomi', 'teboho.mohlomi@email.com', '+266 506-7890', 
                 '987 Heritage Park Quthing 500', 'ID79567890', 'LIC0067890')
            ]
            
            for customer_data in customers:
                customer = Customer(
                    customer_id=customer_data[0],
                    full_name=customer_data[1],
                    email=customer_data[2],
                    phone=customer_data[3],
                    address=customer_data[4],
                    id_number=customer_data[5],
                    license_number=customer_data[6]
                )
                db.session.add(customer)
            print(f"Added {len(customers)} default customers with Sesotho names")
        
        db.session.commit()
        print("Database initialization complete!")

def reset_database():
    """Reset the database by clearing all data and reinitializing"""
    print("Resetting database...")
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("Dropped all tables")
        
        # Recreate tables
        db.create_all()
        print("Created new tables")
        
        # Initialize with default data
        init_database()

def calculate_rental_cost(daily_rate, rental_date, return_date):
    """Calculate rental cost based on dates"""
    days = (return_date - rental_date).days
    if days < 1:
        days = 1
    total = daily_rate * days
    deposit = total * 0.2
    return days, total, deposit

def get_vehicle_stats():
    """Get vehicle statistics"""
    with app.app_context():
        total_vehicles = Vehicle.query.count()
        available_vehicles = Vehicle.query.filter_by(status='Available').count()
        rented_vehicles = Vehicle.query.filter_by(status='Rented').count()
        maintenance_vehicles = Vehicle.query.filter_by(status='Maintenance').count()
        
        return {
            'total': total_vehicles,
            'available': available_vehicles,
            'rented': rented_vehicles,
            'maintenance': maintenance_vehicles
        }

def get_customer_stats():
    """Get customer statistics"""
    with app.app_context():
        total_customers = Customer.query.count()
        active_rentals = Rental.query.filter_by(rental_status='Active').count()
        
        return {
            'total': total_customers,
            'active_rentals': active_rentals
        }

def get_revenue_stats():
    """Get revenue statistics"""
    with app.app_context():
        total_revenue = 0
        pending_payments = 0
        
        completed_payments = Payment.query.filter_by(status='Completed').all()
        for payment in completed_payments:
            total_revenue += payment.amount
        
        pending_rentals = Rental.query.filter_by(payment_status='Pending').count()
        pending_payments = pending_rentals
        
        return {
            'total_revenue': total_revenue,
            'pending_payments': pending_payments
        }

def generate_sesotho_name():
    """Generate a random Sesotho name"""
    first_name = random.choice(SESOTHO_FIRST_NAMES)
    last_name = random.choice(SESOTHO_LAST_NAMES)
    return f"{first_name} {last_name}"

# HTML Templates with FULL CSS styling
BASE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Vehicle Rental Management System{% endblock %}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --primary: #4a00e0;
            --secondary: #8e2de2;
            --success: #00b09b;
            --warning: #f46b45;
            --danger: #e74c3c;
            --dark: #141e30;
            --light: #f8f9fa;
            --gray: #95a5a6;
            --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            --radius: 15px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }

        .flash-messages {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }

        .flash-message {
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            color: white;
            animation: slideIn 0.3s ease;
            max-width: 300px;
            box-shadow: var(--shadow);
        }

        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        .flash-success {
            background: var(--success);
        }

        .flash-error {
            background: var(--danger);
        }

        .flash-info {
            background: var(--primary);
        }

        .flash-warning {
            background: var(--warning);
        }

        .auth-container {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
        }

        .auth-box {
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--radius);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            width: 100%;
            max-width: 500px;
            animation: slideUp 0.5s ease;
        }

        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .auth-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .auth-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            opacity: 0.1;
        }

        .company-logo {
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 10px;
            letter-spacing: 2px;
            position: relative;
            z-index: 1;
        }

        .company-name {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 15px;
            letter-spacing: 1px;
            position: relative;
            z-index: 1;
        }

        .auth-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }

        .auth-subtitle {
            font-size: 14px;
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }

        .auth-body {
            padding: 40px 30px;
            background: white;
        }

        .input-group {
            margin-bottom: 25px;
        }

        .input-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
            font-size: 14px;
        }

        .input-with-icon {
            position: relative;
        }

        .input-icon {
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray);
            font-size: 18px;
            z-index: 1;
        }

        .form-input {
            width: 100%;
            padding: 15px 15px 15px 45px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s;
            background: #f8f9fa;
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 0, 224, 0.1);
            background: white;
        }

        .checkbox-group {
            display: flex;
            align-items: center;
            margin: 20px 0;
        }

        .checkbox-group input {
            margin-right: 10px;
            width: 18px;
            height: 18px;
            accent-color: var(--primary);
        }

        .checkbox-group label {
            font-size: 14px;
            color: var(--dark);
        }

        .btn {
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-align: center;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            text-decoration: none;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            width: 100%;
            position: relative;
            overflow: hidden;
        }

        .btn-primary::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: 0.5s;
        }

        .btn-primary:hover::before {
            left: 100%;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(74, 0, 224, 0.3);
        }

        .btn-primary:active {
            transform: translateY(0);
        }

        .auth-footer {
            margin-top: 25px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 14px;
            color: var(--gray);
            text-align: center;
        }

        .auth-link {
            color: var(--primary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .auth-link:hover {
            text-decoration: underline;
            color: var(--secondary);
        }

        .app-container {
            min-height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .header {
            background: linear-gradient(135deg, var(--dark) 0%, #243b55 100%);
            color: white;
            padding: 0 25px;
            height: 70px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .logo-icon {
            font-size: 24px;
            background: rgba(255, 255, 255, 0.1);
            padding: 10px;
            border-radius: 10px;
            font-weight: bold;
            backdrop-filter: blur(5px);
        }

        .logo-text {
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .user-avatar {
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            color: white;
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }

        .user-details {
            display: flex;
            flex-direction: column;
        }

        .user-name {
            font-weight: 600;
            font-size: 14px;
        }

        .user-role {
            font-size: 12px;
            opacity: 0.8;
        }

        .btn-logout {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            padding: 8px 20px;
            border-radius: 6px;
            font-size: 14px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
            backdrop-filter: blur(5px);
        }

        .btn-logout:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }

        .main-content {
            display: flex;
            min-height: calc(100vh - 70px);
            flex: 1;
        }

        .sidebar {
            width: 250px;
            background: linear-gradient(135deg, #141e30 0%, #243b55 100%);
            color: white;
            overflow-y: auto;
            transition: all 0.3s;
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
        }

        .sidebar-header {
            padding: 30px 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            background: rgba(0, 0, 0, 0.2);
        }

        .sidebar-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin: 0 auto 15px;
            color: white;
            font-weight: bold;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
        }

        .sidebar-welcome {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 5px;
            color: white;
        }

        .sidebar-role {
            font-size: 12px;
            opacity: 0.8;
            padding: 5px 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            display: inline-block;
            backdrop-filter: blur(5px);
        }

        .sidebar-nav {
            padding: 20px 0;
        }

        .nav-btn {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px 25px;
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            transition: all 0.3s;
            border-left: 4px solid transparent;
            cursor: pointer;
            font-size: 14px;
        }

        .nav-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            border-left-color: var(--primary);
            color: white;
            padding-left: 30px;
        }

        .nav-btn.active {
            background: rgba(255, 255, 255, 0.2);
            border-left-color: var(--primary);
            font-weight: 600;
            color: white;
            box-shadow: inset 5px 0 10px rgba(0, 0, 0, 0.1);
        }

        .nav-btn i {
            width: 20px;
            text-align: center;
            font-size: 18px;
        }

        .sidebar-footer {
            padding: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 12px;
            opacity: 0.7;
            text-align: center;
            position: absolute;
            bottom: 0;
            width: 250px;
            background: rgba(0, 0, 0, 0.2);
        }

        .content-area {
            flex: 1;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            overflow-y: auto;
            padding: 30px;
            position: relative;
        }

        .page-title {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 30px;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 15px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(0, 0, 0, 0.1);
            position: relative;
        }

        .page-title::after {
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 100px;
            height: 2px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: white;
            border-radius: var(--radius);
            padding: 25px;
            box-shadow: var(--shadow);
            transition: all 0.3s;
            border-top: 5px solid var(--primary);
            position: relative;
            overflow: hidden;
        }

        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, transparent 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }

        .stat-card:hover::before {
            opacity: 1;
        }

        .stat-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }

        .stat-icon {
            font-size: 36px;
            margin-bottom: 15px;
            display: block;
            color: var(--primary);
        }

        .stat-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 10px;
            color: var(--dark);
            font-family: 'Segoe UI', sans-serif;
        }

        .stat-label {
            color: var(--gray);
            font-size: 14px;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stat-desc {
            color: var(--gray);
            font-size: 12px;
            opacity: 0.8;
        }

        .charts-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-top: 30px;
        }

        .chart-card {
            background: white;
            border-radius: var(--radius);
            padding: 25px;
            box-shadow: var(--shadow);
            transition: transform 0.3s;
        }

        .chart-card:hover {
            transform: translateY(-5px);
        }

        .chart-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .table-container {
            background: white;
            border-radius: var(--radius);
            padding: 25px;
            box-shadow: var(--shadow);
            margin-top: 20px;
            overflow-x: auto;
            position: relative;
        }

        .table-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            flex-wrap: wrap;
            gap: 15px;
        }

        .search-box {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            align-items: center;
        }

        .search-input {
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            min-width: 250px;
            font-size: 14px;
            transition: all 0.3s;
            background: #f8f9fa;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 0, 224, 0.1);
            background: white;
        }

        .btn-search, .btn-clear, .btn-action {
            padding: 12px 25px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.3s;
        }

        .btn-search {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
        }

        .btn-search:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(74, 0, 224, 0.2);
        }

        .btn-clear {
            background: var(--gray);
            color: white;
        }

        .btn-clear:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(149, 165, 166, 0.2);
        }

        .btn-success {
            background: linear-gradient(135deg, var(--success) 0%, #96c93d 100%);
            color: white;
        }

        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0, 176, 155, 0.2);
        }

        .btn-warning {
            background: linear-gradient(135deg, var(--warning) 0%, #ff9966 100%);
            color: white;
        }

        .btn-warning:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(244, 107, 69, 0.2);
        }

        .btn-danger {
            background: linear-gradient(135deg, var(--danger) 0%, #ff6b6b 100%);
            color: white;
        }

        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(231, 76, 60, 0.2);
        }

        .btn-group {
            display: flex;
            gap: 15px;
            margin-top: 25px;
            flex-wrap: wrap;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        }

        .data-table thead {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
        }

        .data-table th {
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border: none;
        }

        .data-table tbody tr {
            transition: all 0.3s;
            border-bottom: 1px solid #f0f0f0;
        }

        .data-table tbody tr:hover {
            background: #f8f9fa;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .data-table td {
            padding: 18px 15px;
            font-size: 14px;
            color: #555;
            border: none;
        }

        .data-table tbody tr:nth-child(even) {
            background: #f9f9f9;
        }

        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: inline-block;
        }

        .status-available, .status-active, .status-completed, .status-paid {
            background: linear-gradient(135deg, var(--success) 0%, rgba(0, 176, 155, 0.2) 100%);
            color: #006b5f;
        }

        .status-rented, .status-pending {
            background: linear-gradient(135deg, var(--warning) 0%, rgba(244, 107, 69, 0.2) 100%);
            color: #b33a1a;
        }

        .status-maintenance, .status-cancelled {
            background: linear-gradient(135deg, var(--danger) 0%, rgba(231, 76, 60, 0.2) 100%);
            color: #c0392b;
        }

        .action-buttons {
            display: flex;
            gap: 8px;
        }

        .btn-icon {
            width: 36px;
            height: 36px;
            border: none;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }

        .btn-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        .form-container {
            background: white;
            border-radius: var(--radius);
            padding: 30px;
            box-shadow: var(--shadow);
            margin-top: 20px;
        }

        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin-bottom: 25px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
            font-size: 14px;
        }

        .form-control {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s;
            background: #f8f9fa;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(74, 0, 224, 0.1);
            background: white;
        }

        .form-control:read-only {
            background: #f5f5f5;
            cursor: not-allowed;
            color: #666;
        }

        .vehicle-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .vehicle-card {
            background: white;
            border-radius: var(--radius);
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: all 0.3s;
        }

        .vehicle-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }

        .vehicle-image {
            height: 150px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 48px;
            position: relative;
            overflow: hidden;
        }

        .vehicle-image::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }

        .vehicle-info {
            padding: 25px;
        }

        .vehicle-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
            color: var(--dark);
        }

        .vehicle-details {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-bottom: 15px;
        }

        .vehicle-detail {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--gray);
            background: #f8f9fa;
            padding: 6px 12px;
            border-radius: 20px;
        }

        .vehicle-price {
            font-size: 24px;
            font-weight: 700;
            color: var(--primary);
            margin-top: 10px;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background: white;
            border-radius: var(--radius);
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            animation: slideUp 0.3s ease;
        }

        .modal-header {
            padding: 25px 30px;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-title {
            font-size: 20px;
            font-weight: 600;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .close-modal {
            background: none;
            border: none;
            color: white;
            font-size: 28px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            border-radius: 50%;
        }

        .close-modal:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: rotate(90deg);
        }

        .modal-content form {
            padding: 30px;
        }

        @media (max-width: 768px) {
            .sidebar {
                width: 70px;
            }
            
            .sidebar-header, .sidebar-footer, .nav-btn span {
                display: none;
            }
            
            .nav-btn {
                justify-content: center;
                padding: 20px;
            }
            
            .nav-btn i {
                font-size: 20px;
            }
            
            .content-area {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .charts-container {
                grid-template-columns: 1fr;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .table-header {
                flex-direction: column;
                align-items: stretch;
            }
            
            .search-box {
                flex-direction: column;
            }
            
            .search-input {
                min-width: auto;
            }
            
            .btn-group {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
        }

        @media (max-width: 480px) {
            .header {
                padding: 0 15px;
            }
            
            .logo-text {
                display: none;
            }
            
            .user-details {
                display: none;
            }
            
            .auth-box {
                margin: 10px;
            }
            
            .auth-header {
                padding: 30px 20px;
            }
            
            .auth-body {
                padding: 30px 20px;
            }
            
            .page-title {
                font-size: 24px;
            }
        }

        /* Animation for loading */
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        .loading {
            animation: pulse 1.5s infinite;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%);
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Flash Messages -->
    <div class="flash-messages">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash-message flash-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
    </div>

    {% block content %}{% endblock %}
    
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# Routes
@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, full_name, password]):
            flash('All fields are required!', 'error')
            return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
                {% block content %}
                <div class="auth-container">
                    <div class="auth-box">
                        <div class="auth-header">
                            <div class="company-logo">VRS</div>
                            <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                            <h1 class="auth-title">Create Account</h1>
                            <p class="auth-subtitle">Join Vehicle Rental System</p>
                        </div>
                        
                        <div class="auth-body">
                            <form method="POST" action="{{ url_for('register') }}">
                                <div class="input-group">
                                    <label class="input-label">Full Name</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-user"></i></span>
                                        <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Username</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-user-circle"></i></span>
                                        <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Email Address</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-envelope"></i></span>
                                        <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Password</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-lock"></i></span>
                                        <input type="password" name="password" id="password" class="form-input" placeholder="Create a password" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Confirm Password</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-lock"></i></span>
                                        <input type="password" name="confirm_password" id="confirm_password" class="form-input" placeholder="Confirm your password" required>
                                    </div>
                                </div>
                                
                                <div class="checkbox-group">
                                    <input type="checkbox" id="showPasswords" onchange="togglePasswords()">
                                    <label for="showPasswords">Show Passwords</label>
                                </div>
                                
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-user-plus"></i>
                                    REGISTER ACCOUNT
                                </button>
                            </form>
                            
                            <div class="auth-footer">
                                <p>Already have an account? <a href="{{ url_for('login') }}" class="auth-link">Login here</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    function togglePasswords() {
                        const show = document.getElementById('showPasswords').checked;
                        document.getElementById('password').type = show ? 'text' : 'password';
                        document.getElementById('confirm_password').type = show ? 'text' : 'password';
                    }
                </script>
                {% endblock %}
            '''))
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
                {% block content %}
                <div class="auth-container">
                    <div class="auth-box">
                        <div class="auth-header">
                            <div class="company-logo">VRS</div>
                            <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                            <h1 class="auth-title">Create Account</h1>
                            <p class="auth-subtitle">Join Vehicle Rental System</p>
                        </div>
                        
                        <div class="auth-body">
                            <form method="POST" action="{{ url_for('register') }}">
                                <div class="input-group">
                                    <label class="input-label">Full Name</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-user"></i></span>
                                        <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Username</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-user-circle"></i></span>
                                        <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Email Address</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-envelope"></i></span>
                                        <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Password</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-lock"></i></span>
                                        <input type="password" name="password" id="password" class="form-input" placeholder="Create a password" required>
                                    </div>
                                </div>
                                
                                <div class="input-group">
                                    <label class="input-label">Confirm Password</label>
                                    <div class="input-with-icon">
                                        <span class="input-icon"><i class="fas fa-lock"></i></span>
                                        <input type="password" name="confirm_password" id="confirm_password" class="form-input" placeholder="Confirm your password" required>
                                    </div>
                                </div>
                                
                                <div class="checkbox-group">
                                    <input type="checkbox" id="showPasswords" onchange="togglePasswords()">
                                    <label for="showPasswords">Show Passwords</label>
                                </div>
                                
                                <button type="submit" class="btn btn-primary">
                                    <i class="fas fa-user-plus"></i>
                                    REGISTER ACCOUNT
                                </button>
                            </form>
                            
                            <div class="auth-footer">
                                <p>Already have an account? <a href="{{ url_for('login') }}" class="auth-link">Login here</a></p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <script>
                    function togglePasswords() {
                        const show = document.getElementById('showPasswords').checked;
                        document.getElementById('password').type = show ? 'text' : 'password';
                        document.getElementById('confirm_password').type = show ? 'text' : 'password';
                    }
                </script>
                {% endblock %}
            '''))
        
        with app.app_context():
            if User.query.filter_by(username=username).first():
                flash('Username already exists!', 'error')
                return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
                    {% block content %}
                    <div class="auth-container">
                        <div class="auth-box">
                            <div class="auth-header">
                                <div class="company-logo">VRS</div>
                                <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                                <h1 class="auth-title">Create Account</h1>
                                <p class="auth-subtitle">Join Vehicle Rental System</p>
                            </div>
                            
                            <div class="auth-body">
                                <form method="POST" action="{{ url_for('register') }}">
                                    <div class="input-group">
                                        <label class="input-label">Full Name</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-user"></i></span>
                                            <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Username</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-user-circle"></i></span>
                                            <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Email Address</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-envelope"></i></span>
                                            <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Password</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-lock"></i></span>
                                            <input type="password" name="password" id="password" class="form-input" placeholder="Create a password" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Confirm Password</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-lock"></i></span>
                                            <input type="password" name="confirm_password" id="confirm_password" class="form-input" placeholder="Confirm your password" required>
                                        </div>
                                    </div>
                                    
                                    <div class="checkbox-group">
                                        <input type="checkbox" id="showPasswords" onchange="togglePasswords()">
                                        <label for="showPasswords">Show Passwords</label>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-user-plus"></i>
                                        REGISTER ACCOUNT
                                    </button>
                                </form>
                                
                                <div class="auth-footer">
                                    <p>Already have an account? <a href="{{ url_for('login') }}" class="auth-link">Login here</a></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <script>
                        function togglePasswords() {
                            const show = document.getElementById('showPasswords').checked;
                            document.getElementById('password').type = show ? 'text' : 'password';
                            document.getElementById('confirm_password').type = show ? 'text' : 'password';
                        }
                    </script>
                    {% endblock %}
                '''))
            
            if User.query.filter_by(email=email).first():
                flash('Email already exists!', 'error')
                return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
                    {% block content %}
                    <div class="auth-container">
                        <div class="auth-box">
                            <div class="auth-header">
                                <div class="company-logo">VRS</div>
                                <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                                <h1 class="auth-title">Create Account</h1>
                                <p class="auth-subtitle">Join Vehicle Rental System</p>
                            </div>
                            
                            <div class="auth-body">
                                <form method="POST" action="{{ url_for('register') }}">
                                    <div class="input-group">
                                        <label class="input-label">Full Name</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-user"></i></span>
                                            <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Username</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-user-circle"></i></span>
                                            <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Email Address</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-envelope"></i></span>
                                            <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Password</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-lock"></i></span>
                                            <input type="password" name="password" id="password" class="form-input" placeholder="Create a password" required>
                                        </div>
                                    </div>
                                    
                                    <div class="input-group">
                                        <label class="input-label">Confirm Password</label>
                                        <div class="input-with-icon">
                                            <span class="input-icon"><i class="fas fa-lock"></i></span>
                                            <input type="password" name="confirm_password" id="confirm_password" class="form-input" placeholder="Confirm your password" required>
                                        </div>
                                    </div>
                                    
                                    <div class="checkbox-group">
                                        <input type="checkbox" id="showPasswords" onchange="togglePasswords()">
                                        <label for="showPasswords">Show Passwords</label>
                                    </div>
                                    
                                    <button type="submit" class="btn btn-primary">
                                        <i class="fas fa-user-plus"></i>
                                        REGISTER ACCOUNT
                                    </button>
                                </form>
                                
                                <div class="auth-footer">
                                    <p>Already have an account? <a href="{{ url_for('login') }}" class="auth-link">Login here</a></p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <script>
                        function togglePasswords() {
                            const show = document.getElementById('showPasswords').checked;
                            document.getElementById('password').type = show ? 'text' : 'password';
                            document.getElementById('confirm_password').type = show ? 'text' : 'password';
                        }
                    </script>
                    {% endblock %}
                '''))
            
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                role='employee'
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        {% block content %}
        <div class="auth-container">
            <div class="auth-box">
                <div class="auth-header">
                    <div class="company-logo">VRS</div>
                    <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                    <h1 class="auth-title">Create Account</h1>
                    <p class="auth-subtitle">Join Vehicle Rental System</p>
                </div>
                
                <div class="auth-body">
                    <form method="POST" action="{{ url_for('register') }}">
                        <div class="input-group">
                            <label class="input-label">Full Name</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-user"></i></span>
                                <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <label class="input-label">Username</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-user-circle"></i></span>
                                <input type="text" name="username" class="form-input" placeholder="Choose a username" required>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <label class="input-label">Email Address</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-envelope"></i></span>
                                <input type="email" name="email" class="form-input" placeholder="Enter your email" required>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <label class="input-label">Password</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-lock"></i></span>
                                <input type="password" name="password" id="password" class="form-input" placeholder="Create a password" required>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <label class="input-label">Confirm Password</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-lock"></i></span>
                                <input type="password" name="confirm_password" id="confirm_password" class="form-input" placeholder="Confirm your password" required>
                            </div>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" id="showPasswords" onchange="togglePasswords()">
                            <label for="showPasswords">Show Passwords</label>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-user-plus"></i>
                            REGISTER ACCOUNT
                        </button>
                    </form>
                    
                    <div class="auth-footer">
                        <p>Already have an account? <a href="{{ url_for('login') }}" class="auth-link">Login here</a></p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function togglePasswords() {
                const show = document.getElementById('showPasswords').checked;
                document.getElementById('password').type = show ? 'text' : 'password';
                document.getElementById('confirm_password').type = show ? 'text' : 'password';
            }
        </script>
        {% endblock %}
    '''))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        with app.app_context():
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['full_name'] = user.full_name
                session['role'] = user.role
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password!', 'error')
    
    return render_template_string(BASE_TEMPLATE.replace('{% block content %}{% endblock %}', '''
        {% block content %}
        <div class="auth-container">
            <div class="auth-box">
                <div class="auth-header">
                    <div class="company-logo">VRS</div>
                    <div class="company-name">VEHICLE RENTAL SYSTEM</div>
                    <h1 class="auth-title">Vehicle Rental Management</h1>
                    <p class="auth-subtitle">Enterprise Vehicle Rental Solution</p>
                </div>
                
                <div class="auth-body">
                    <form method="POST" action="{{ url_for('login') }}">
                        <div class="input-group">
                            <label class="input-label">Username</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-user"></i></span>
                                <input type="text" name="username" class="form-input" placeholder="Enter your username" required>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <label class="input-label">Password</label>
                            <div class="input-with-icon">
                                <span class="input-icon"><i class="fas fa-lock"></i></span>
                                <input type="password" name="password" id="password" class="form-input" placeholder="Enter your password" required>
                            </div>
                        </div>
                        
                        <div class="checkbox-group">
                            <input type="checkbox" id="showPassword" onchange="togglePassword()">
                            <label for="showPassword">Show Password</label>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-sign-in-alt"></i>
                            LOGIN TO SYSTEM
                        </button>
                    </form>
                    
                    <div class="auth-footer">
                        <p>Don't have an account? <a href="{{ url_for('register') }}" class="auth-link">Register here</a></p>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            function togglePassword() {
                const passwordField = document.getElementById('password');
                passwordField.type = document.getElementById('showPassword').checked ? 'text' : 'password';
            }
            
            // Login on Enter key
            document.getElementById('password').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    document.querySelector('form').submit();
                }
            });
        </script>
        {% endblock %}
    '''))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    vehicle_stats = get_vehicle_stats()
    customer_stats = get_customer_stats()
    revenue_stats = get_revenue_stats()
    
    with app.app_context():
        active_rentals_count = Rental.query.filter_by(rental_status='Active').count()
        completed_rentals_count = Rental.query.filter_by(rental_status='Completed').count()
        cancelled_rentals_count = Rental.query.filter_by(rental_status='Cancelled').count()
        
        recent_rentals = Rental.query.order_by(Rental.created_at.desc()).limit(5).all()
    
    dashboard_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn active">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                    </a>
                    <a href="{{ url_for('reports') }}" class="nav-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>Reports</span>
                    </a>
                </div>
                
                <div class="sidebar-footer">
                    <div>© 2024 VEHICLE RENTAL</div>
                    <div>Version 2.0.1</div>
                </div>
            </nav>
            
            <main class="content-area">
                <h1 class="page-title"><i class="fas fa-chart-bar"></i> Dashboard Overview</h1>
                
                <div class="stats-grid">
                    <div class="stat-card" style="border-top-color: var(--primary);">
                        <span class="stat-icon"><i class="fas fa-car"></i></span>
                        <div class="stat-value">{{ vehicle_stats.available }}</div>
                        <div class="stat-label">Available Vehicles</div>
                        <div class="stat-desc">Total: {{ vehicle_stats.total }}</div>
                    </div>
                    
                    <div class="stat-card" style="border-top-color: var(--secondary);">
                        <span class="stat-icon"><i class="fas fa-users"></i></span>
                        <div class="stat-value">{{ customer_stats.total }}</div>
                        <div class="stat-label">Total Customers</div>
                        <div class="stat-desc">{{ customer_stats.active_rentals }} Active Rentals</div>
                    </div>
                    
                    <div class="stat-card" style="border-top-color: var(--success);">
                        <span class="stat-icon"><i class="fas fa-money-bill-wave"></i></span>
                        <div class="stat-value">R {{ "%.2f"|format(revenue_stats.total_revenue) }}</div>
                        <div class="stat-label">Total Revenue</div>
                        <div class="stat-desc">{{ revenue_stats.pending_payments }} Pending</div>
                    </div>
                    
                    <div class="stat-card" style="border-top-color: var(--warning);">
                        <span class="stat-icon"><i class="fas fa-clock"></i></span>
                        <div class="stat-value">{{ active_rentals_count }}</div>
                        <div class="stat-label">Active Rentals</div>
                        <div class="stat-desc">{{ completed_rentals_count }} Completed</div>
                    </div>
                </div>
                
                <div class="charts-container">
                    <div class="chart-card">
                        <h3 class="chart-title"><i class="fas fa-chart-pie"></i> Vehicle Status Distribution</h3>
                        <canvas id="vehicleChart"></canvas>
                    </div>
                    
                    <div class="chart-card">
                        <h3 class="chart-title"><i class="fas fa-chart-bar"></i> Rental Status Overview</h3>
                        <canvas id="rentalChart"></canvas>
                    </div>
                </div>
                
                <div class="table-container" style="margin-top: 30px;">
                    <div class="table-header">
                        <h3 style="color: var(--dark);">Recent Rentals</h3>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Rental ID</th>
                                <th>Customer</th>
                                <th>Vehicle</th>
                                <th>Period</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for rental in recent_rentals %}
                            <tr>
                                <td>{{ rental.rental_id }}</td>
                                <td>{{ rental.customer_name }}</td>
                                <td>{{ rental.vehicle_info }}</td>
                                <td>{{ rental.rental_date.strftime('%Y-%m-%d') }} to {{ rental.return_date.strftime('%Y-%m-%d') }}</td>
                                <td>R {{ "%.2f"|format(rental.total_amount) }}</td>
                                <td><span class="status-badge status-{{ rental.rental_status.lower() }}">{{ rental.rental_status }}</span></td>
                                <td>{{ rental.created_at.strftime('%Y-%m-%d') }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="form-container" style="margin-top: 30px;">
                    <h3 style="color: var(--dark); margin-bottom: 20px;"><i class="fas fa-bolt"></i> Quick Actions</h3>
                    <div class="btn-group">
                        <a href="{{ url_for('rent_vehicle') }}" class="btn btn-primary">
                            <i class="fas fa-car"></i> Rent Vehicle
                        </a>
                        <a href="{{ url_for('add_random_vehicle') }}" class="btn btn-success" onclick="return confirm('Add a random vehicle?')">
                            <i class="fas fa-car-side"></i> Add Random Vehicle
                        </a>
                        <a href="{{ url_for('add_random_customer') }}" class="btn btn-warning" onclick="return confirm('Add a random customer with Sesotho name?')">
                            <i class="fas fa-user-plus"></i> Add Random Customer
                        </a>
                        <a href="{{ url_for('payments') }}" class="btn btn-primary">
                            <i class="fas fa-money-bill-wave"></i> Process Payment
                        </a>
                    </div>
                </div>
            </main>
        </div>
    </div>
    
    <script>
        // Vehicle Status Chart
        const vehicleCtx = document.getElementById('vehicleChart').getContext('2d');
        new Chart(vehicleCtx, {
            type: 'pie',
            data: {
                labels: ['Available', 'Rented', 'Maintenance'],
                datasets: [{
                    data: [{{ vehicle_stats.available }}, {{ vehicle_stats.rented }}, {{ vehicle_stats.maintenance }}],
                    backgroundColor: [
                        '#00b09b',
                        '#4a00e0',
                        '#f46b45'
                    ],
                    borderWidth: 2,
                    borderColor: 'white'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        // Rental Status Chart
        const rentalCtx = document.getElementById('rentalChart').getContext('2d');
        new Chart(rentalCtx, {
            type: 'bar',
            data: {
                labels: ['Active', 'Completed', 'Cancelled'],
                datasets: [{
                    label: 'Number of Rentals',
                    data: [{{ active_rentals_count }}, {{ completed_rentals_count }}, {{ cancelled_rentals_count }}],
                    backgroundColor: '#4a00e0',
                    borderColor: '#8e2de2',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    </script>
    {% endblock %}
    '''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', dashboard_template),
        vehicle_stats=vehicle_stats,
        customer_stats=customer_stats,
        revenue_stats=revenue_stats,
        active_rentals_count=active_rentals_count,
        completed_rentals_count=completed_rentals_count,
        cancelled_rentals_count=cancelled_rentals_count,
        recent_rentals=recent_rentals
    )

@app.route('/rent_vehicle')
def rent_vehicle():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with app.app_context():
        customers = Customer.query.all()
        available_vehicles = Vehicle.query.filter_by(status='Available').all()
    
    rent_vehicle_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn active">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                    </a>
                    <a href="{{ url_for('reports') }}" class="nav-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>Reports</span>
                    </a>
                </div>
                
                <div class="sidebar-footer">
                    <div>© 2024 VEHICLE RENTAL</div>
                    <div>Version 2.0.1</div>
                </div>
            </nav>
            
            <main class="content-area">
                <h1 class="page-title"><i class="fas fa-car"></i> Rent a Vehicle</h1>
                
                <div class="form-container">
                    <form method="POST" action="{{ url_for('process_rental') }}">
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Select Customer</label>
                                <select name="customer_id" class="form-control" required onchange="updateCustomerInfo()" id="customerSelect">
                                    <option value="">Select Customer</option>
                                    {% for customer in customers %}
                                    <option value="{{ customer.customer_id }}" data-name="{{ customer.full_name }}" data-phone="{{ customer.phone }}" data-email="{{ customer.email }}">
                                        {{ customer.customer_id }} - {{ customer.full_name }}
                                    </option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Customer Name</label>
                                <input type="text" class="form-control" id="customerName" readonly>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Customer Phone</label>
                                <input type="text" class="form-control" id="customerPhone" readonly>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Customer Email</label>
                                <input type="email" class="form-control" id="customerEmail" readonly>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Select Vehicle</label>
                                <select name="vehicle_id" class="form-control" required onchange="updateVehicleInfo()" id="vehicleSelect">
                                    <option value="">Select Vehicle</option>
                                    {% for vehicle in available_vehicles %}
                                    <option value="{{ vehicle.vehicle_id }}" data-info="{{ vehicle.make }} {{ vehicle.model }} {{ vehicle.year }}" data-rate="{{ vehicle.daily_rate }}" data-plate="{{ vehicle.plate_number }}">
                                        {{ vehicle.vehicle_id }} - {{ vehicle.make }} {{ vehicle.model }} ({{ vehicle.plate_number }}) - R{{ vehicle.daily_rate }}/day
                                    </option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Vehicle Info</label>
                                <input type="text" class="form-control" id="vehicleInfo" readonly>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Plate Number</label>
                                <input type="text" class="form-control" id="plateNumber" readonly>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Daily Rate</label>
                                <input type="text" class="form-control" id="dailyRate" readonly>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Rental Date</label>
                                <input type="date" name="rental_date" class="form-control" required id="rentalDate" onchange="calculateCost()">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Return Date</label>
                                <input type="date" name="return_date" class="form-control" required id="returnDate" onchange="calculateCost()">
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Total Days</label>
                                <input type="text" class="form-control" id="totalDays" readonly>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Total Amount</label>
                                <input type="text" class="form-control" id="totalAmount" readonly>
                            </div>
                        </div>
                        
                        <div class="form-row">
                            <div class="form-group">
                                <label class="form-label">Deposit (20%)</label>
                                <input type="text" class="form-control" id="depositAmount" readonly>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Payment Method</label>
                                <select name="payment_method" class="form-control" required>
                                    <option value="Cash">Cash</option>
                                    <option value="Credit Card">Credit Card</option>
                                    <option value="Mobile Money">Mobile Money</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="btn-group">
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-check-circle"></i> Process Rental
                            </button>
                            <button type="button" class="btn btn-clear" onclick="resetForm()">
                                <i class="fas fa-redo"></i> Reset Form
                            </button>
                            <a href="{{ url_for('add_random_customer') }}" class="btn btn-primary" onclick="return confirm('Add a random customer with Sesotho name?')">
                                <i class="fas fa-user-plus"></i> Add Random Customer
                            </a>
                        </div>
                    </form>
                </div>
            </main>
        </div>
    </div>
    
    <script>
        function updateCustomerInfo() {
            const select = document.getElementById('customerSelect');
            const selectedOption = select.options[select.selectedIndex];
            
            if (selectedOption.value) {
                document.getElementById('customerName').value = selectedOption.getAttribute('data-name');
                document.getElementById('customerPhone').value = selectedOption.getAttribute('data-phone');
                document.getElementById('customerEmail').value = selectedOption.getAttribute('data-email');
            } else {
                document.getElementById('customerName').value = '';
                document.getElementById('customerPhone').value = '';
                document.getElementById('customerEmail').value = '';
            }
        }
        
        function updateVehicleInfo() {
            const select = document.getElementById('vehicleSelect');
            const selectedOption = select.options[select.selectedIndex];
            
            if (selectedOption.value) {
                document.getElementById('vehicleInfo').value = selectedOption.getAttribute('data-info');
                document.getElementById('plateNumber').value = selectedOption.getAttribute('data-plate');
                document.getElementById('dailyRate').value = 'R ' + selectedOption.getAttribute('data-rate');
                calculateCost();
            } else {
                document.getElementById('vehicleInfo').value = '';
                document.getElementById('plateNumber').value = '';
                document.getElementById('dailyRate').value = '';
                resetCost();
            }
        }
        
        function calculateCost() {
            const rentalDate = new Date(document.getElementById('rentalDate').value);
            const returnDate = new Date(document.getElementById('returnDate').value);
            const dailyRate = parseFloat(document.getElementById('dailyRate').value.replace('R ', '')) || 0;
            
            if (rentalDate && returnDate && dailyRate > 0 && returnDate > rentalDate) {
                const timeDiff = returnDate.getTime() - rentalDate.getTime();
                const dayDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
                const totalAmount = dayDiff * dailyRate;
                const deposit = totalAmount * 0.2;
                
                document.getElementById('totalDays').value = dayDiff + ' days';
                document.getElementById('totalAmount').value = 'R ' + totalAmount.toFixed(2);
                document.getElementById('depositAmount').value = 'R ' + deposit.toFixed(2);
            } else {
                resetCost();
            }
        }
        
        function resetCost() {
            document.getElementById('totalDays').value = '';
            document.getElementById('totalAmount').value = '';
            document.getElementById('depositAmount').value = '';
        }
        
        function resetForm() {
            document.querySelector('form').reset();
            document.getElementById('customerName').value = '';
            document.getElementById('customerPhone').value = '';
            document.getElementById('customerEmail').value = '';
            document.getElementById('vehicleInfo').value = '';
            document.getElementById('plateNumber').value = '';
            document.getElementById('dailyRate').value = '';
            resetCost();
        }
        
        // Set default dates
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        
        document.getElementById('rentalDate').value = today.toISOString().split('T')[0];
        document.getElementById('returnDate').value = tomorrow.toISOString().split('T')[0];
    </script>
    {% endblock %}
    '''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', rent_vehicle_template),
        customers=customers,
        available_vehicles=available_vehicles
    )

@app.route('/process_rental', methods=['POST'])
def process_rental():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        customer_id = request.form.get('customer_id')
        vehicle_id = request.form.get('vehicle_id')
        rental_date = datetime.strptime(request.form.get('rental_date'), '%Y-%m-%d').date()
        return_date = datetime.strptime(request.form.get('return_date'), '%Y-%m-%d').date()
        payment_method = request.form.get('payment_method')
        
        with app.app_context():
            customer = Customer.query.filter_by(customer_id=customer_id).first()
            vehicle = Vehicle.query.filter_by(vehicle_id=vehicle_id).first()
            
            if not customer or not vehicle:
                flash('Invalid customer or vehicle selected!', 'error')
                return redirect(url_for('rent_vehicle'))
            
            daily_rate = vehicle.daily_rate
            total_days, total_amount, deposit = calculate_rental_cost(daily_rate, rental_date, return_date)
            
            last_rental = Rental.query.order_by(Rental.id.desc()).first()
            if last_rental:
                last_num = int(last_rental.rental_id[2:]) if last_rental.rental_id.startswith('RN') else 0
                rental_id = f"RN{str(last_num + 1).zfill(4)}"
            else:
                rental_id = "RN0001"
            
            rental = Rental(
                rental_id=rental_id,
                customer_id=customer_id,
                customer_name=customer.full_name,
                vehicle_id=vehicle_id,
                vehicle_info=f"{vehicle.make} {vehicle.model} ({vehicle.plate_number})",
                rental_date=rental_date,
                return_date=return_date,
                daily_rate=daily_rate,
                total_days=total_days,
                total_amount=total_amount,
                deposit=deposit,
                payment_status='Pending',
                rental_status='Active'
            )
            
            vehicle.status = 'Rented'
            
            db.session.add(rental)
            db.session.commit()
        
        flash(f'Vehicle rented successfully! Rental ID: {rental_id}', 'success')
        return redirect(url_for('dashboard'))
    
    except Exception as e:
        flash(f'Error processing rental: {str(e)}', 'error')
        return redirect(url_for('rent_vehicle'))

@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with app.app_context():
        vehicles_list = Vehicle.query.all()
    
    vehicles_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn active">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                    </a>
                    <a href="{{ url_for('reports') }}" class="nav-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>Reports</span>
                    </a>
                </div>
                
                <div class="sidebar-footer">
                    <div>© 2024 VEHICLE RENTAL</div>
                    <div>Version 2.0.1</div>
                </div>
            </nav>
            
            <main class="content-area">
                <h1 class="page-title"><i class="fas fa-car-side"></i> Vehicle Management</h1>
                
                <div class="table-container">
                    <div class="table-header">
                        <h3 style="color: var(--dark);">All Vehicles</h3>
                        <div class="search-box">
                            <button class="btn btn-primary" onclick="showAddVehicleModal()">
                                <i class="fas fa-car-side"></i> Add Vehicle
                            </button>
                            <button class="btn btn-success" onclick="window.location.href='/add_random_vehicle'" style="margin-left: 10px;">
                                <i class="fas fa-random"></i> Add Random Vehicle
                            </button>
                        </div>
                    </div>
                    
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Make & Model</th>
                                <th>Year</th>
                                <th>Color</th>
                                <th>Plate</th>
                                <th>Daily Rate</th>
                                <th>Status</th>
                                <th>Fuel Type</th>
                                <th>Transmission</th>
                                <th>Seats</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for vehicle in vehicles %}
                            <tr>
                                <td>{{ vehicle.vehicle_id }}</td>
                                <td>{{ vehicle.make }} {{ vehicle.model }}</td>
                                <td>{{ vehicle.year }}</td>
                                <td>{{ vehicle.color }}</td>
                                <td>{{ vehicle.plate_number }}</td>
                                <td>R {{ "%.2f"|format(vehicle.daily_rate) }}</td>
                                <td><span class="status-badge status-{{ vehicle.status.lower() }}">{{ vehicle.status }}</span></td>
                                <td>{{ vehicle.fuel_type }}</td>
                                <td>{{ vehicle.transmission }}</td>
                                <td>{{ vehicle.seats }}</td>
                                <td>
                                    <div class="action-buttons">
                                        <button class="btn-icon btn-success" onclick="editVehicle('{{ vehicle.vehicle_id }}')" title="Edit">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn-icon btn-danger" onclick="deleteVehicle('{{ vehicle.vehicle_id }}')" title="Delete">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="vehicle-grid" style="margin-top: 30px;">
                    {% for vehicle in vehicles %}
                    <div class="vehicle-card">
                        <div class="vehicle-image">
                            <i class="fas fa-car"></i>
                        </div>
                        <div class="vehicle-info">
                            <h3 class="vehicle-title">{{ vehicle.make }} {{ vehicle.model }} ({{ vehicle.year }})</h3>
                            <div class="vehicle-details">
                                <span class="vehicle-detail">
                                    <i class="fas fa-tag"></i> {{ vehicle.plate_number }}
                                </span>
                                <span class="vehicle-detail">
                                    <i class="fas fa-gas-pump"></i> {{ vehicle.fuel_type }}
                                </span>
                                <span class="vehicle-detail">
                                    <i class="fas fa-cogs"></i> {{ vehicle.transmission }}
                                </span>
                                <span class="vehicle-detail">
                                    <i class="fas fa-user-friends"></i> {{ vehicle.seats }} seats
                                </span>
                            </div>
                            <div class="vehicle-price">
                                R {{ "%.2f"|format(vehicle.daily_rate) }} / day
                            </div>
                            <div style="margin-top: 10px;">
                                <span class="status-badge status-{{ vehicle.status.lower() }}">
                                    {{ vehicle.status }}
                                </span>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </main>
        </div>
    </div>
    
    <!-- Add Vehicle Modal -->
    <div id="addVehicleModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title"><i class="fas fa-car-side"></i> Add New Vehicle</h3>
                <button class="close-modal" onclick="closeModal('addVehicleModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_vehicle') }}">
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Make</label>
                        <input type="text" name="make" class="form-control" required placeholder="e.g., Toyota">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Model</label>
                        <input type="text" name="model" class="form-control" required placeholder="e.g., Corolla">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Year</label>
                        <input type="number" name="year" class="form-control" required min="2000" max="2024" value="2023">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Color</label>
                        <input type="text" name="color" class="form-control" required placeholder="e.g., White">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Plate Number</label>
                        <input type="text" name="plate_number" class="form-control" required placeholder="e.g., ABC123">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Daily Rate (R)</label>
                        <input type="number" name="daily_rate" class="form-control" required min="500" step="100" value="1500">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Fuel Type</label>
                        <select name="fuel_type" class="form-control" required>
                            <option value="Petrol">Petrol</option>
                            <option value="Diesel">Diesel</option>
                            <option value="Electric">Electric</option>
                            <option value="Hybrid">Hybrid</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Transmission</label>
                        <select name="transmission" class="form-control" required>
                            <option value="Automatic">Automatic</option>
                            <option value="Manual">Manual</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Seats</label>
                        <input type="number" name="seats" class="form-control" required min="2" max="20" value="5">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Status</label>
                        <select name="status" class="form-control" required>
                            <option value="Available">Available</option>
                            <option value="Maintenance">Maintenance</option>
                            <option value="Rented">Rented</option>
                        </select>
                    </div>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Save Vehicle
                    </button>
                    <button type="button" class="btn btn-clear" onclick="closeModal('addVehicleModal')">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        function showAddVehicleModal() {
            document.getElementById('addVehicleModal').style.display = 'flex';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        function editVehicle(vehicleId) {
            alert('Edit vehicle: ' + vehicleId + ' (Functionality to be implemented)');
            // Implement edit vehicle functionality
        }
        
        function deleteVehicle(vehicleId) {
            if (confirm('Are you sure you want to delete vehicle ' + vehicleId + '?')) {
                alert('Delete vehicle: ' + vehicleId + ' (Functionality to be implemented)');
                // Implement delete vehicle functionality
            }
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        };
    </script>
    {% endblock %}
    '''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', vehicles_template),
        vehicles=vehicles_list
    )

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with app.app_context():
            last_vehicle = Vehicle.query.order_by(Vehicle.id.desc()).first()
            if last_vehicle:
                last_num = int(last_vehicle.vehicle_id[1:])
                new_id = f"V{str(last_num + 1).zfill(3)}"
            else:
                new_id = "V006"
            
            vehicle = Vehicle(
                vehicle_id=new_id,
                make=request.form.get('make'),
                model=request.form.get('model'),
                year=int(request.form.get('year')),
                color=request.form.get('color'),
                plate_number=request.form.get('plate_number'),
                daily_rate=float(request.form.get('daily_rate')),
                status=request.form.get('status'),
                fuel_type=request.form.get('fuel_type'),
                transmission=request.form.get('transmission'),
                seats=int(request.form.get('seats'))
            )
            
            db.session.add(vehicle)
            db.session.commit()
        
        flash('Vehicle added successfully!', 'success')
        return redirect(url_for('vehicles'))
    
    except Exception as e:
        flash(f'Error adding vehicle: {str(e)}', 'error')
        return redirect(url_for('vehicles'))

@app.route('/customers')
def customers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with app.app_context():
        customers_list = Customer.query.all()
        
        # Calculate active rentals count
        active_rentals_count = Rental.query.filter_by(rental_status='Active').count()
    
    customers_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn active">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                    </a>
                    <a href="{{ url_for('reports') }}" class="nav-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>Reports</span>
                    </a>
                </div>
                
                <div class="sidebar-footer">
                    <div>© 2024 VEHICLE RENTAL</div>
                    <div>Version 2.0.1</div>
                </div>
            </nav>
            
            <main class="content-area">
                <h1 class="page-title"><i class="fas fa-users"></i> Customer Management</h1>
                
                <div class="table-container">
                    <div class="table-header">
                        <h3 style="color: var(--dark);">Customer List</h3>
                        <div class="search-box">
                            <input type="text" id="customerSearch" class="search-input" placeholder="Search customers...">
                            <button class="btn-search" onclick="searchCustomers()">
                                <i class="fas fa-search"></i> Search
                            </button>
                            <button class="btn btn-primary" onclick="showAddCustomerModal()">
                                <i class="fas fa-user-plus"></i> Add Customer
                            </button>
                            <button class="btn btn-success" onclick="window.location.href='/add_random_customer'" style="margin-left: 10px;">
                                <i class="fas fa-random"></i> Add Random Customer
                            </button>
                        </div>
                    </div>
                    
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Phone</th>
                                <th>Email</th>
                                <th>ID Number</th>
                                <th>License</th>
                                <th>Status</th>
                                <th>Registered</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="customerTableBody">
                            {% for customer in customers %}
                            <tr>
                                <td>{{ customer.customer_id }}</td>
                                <td>{{ customer.full_name }}</td>
                                <td>{{ customer.phone }}</td>
                                <td>{{ customer.email }}</td>
                                <td>{{ customer.id_number }}</td>
                                <td>{{ customer.license_number }}</td>
                                <td><span class="status-badge status-active">{{ customer.status }}</span></td>
                                <td>{{ customer.created_at.strftime('%Y-%m-%d') }}</td>
                                <td>
                                    <div class="action-buttons">
                                        <button class="btn-icon btn-warning" onclick="editCustomer('{{ customer.customer_id }}')" title="Edit">
                                            <i class="fas fa-edit"></i>
                                        </button>
                                        <button class="btn-icon btn-danger" onclick="deleteCustomer('{{ customer.customer_id }}')" title="Delete">
                                            <i class="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <!-- At a Glance Section - Replaced AI-sounding text -->
                <div class="form-container" style="margin-top: 30px;">
                    <h3 style="color: var(--dark); margin-bottom: 20px;"><i class="fas fa-chart-simple"></i> At a Glance</h3>
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;">
                            <div>
                                <p style="font-size: 14px; color: var(--gray); margin-bottom: 5px;">Total Customers</p>
                                <p style="font-size: 28px; font-weight: 700; color: var(--primary);">{{ customers|length }}</p>
                            </div>
                            <div>
                                <p style="font-size: 14px; color: var(--gray); margin-bottom: 5px;">Active Rentals</p>
                                <p style="font-size: 28px; font-weight: 700; color: var(--success);">{{ active_rentals_count }}</p>
                            </div>
                        </div>
                        
                        <div style="border-top: 1px solid #dee2e6; padding-top: 15px;">
                            <p style="font-size: 14px; color: var(--gray); margin-bottom: 10px;"><i class="fas fa-users" style="margin-right: 8px; color: var(--primary);"></i>Recent Customers:</p>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                                {% for customer in customers[:3] %}
                                <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                                    {{ customer.full_name.split(' ')[0] }}
                                </span>
                                {% endfor %}
                                {% if customers|length > 3 %}
                                <span style="background: white; padding: 5px 12px; border-radius: 20px; font-size: 13px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                                    +{{ customers|length - 3 }} more
                                </span>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div style="margin-top: 15px; font-size: 13px; color: var(--gray); background: white; padding: 10px; border-radius: 8px;">
                            <i class="fas fa-calendar-check" style="margin-right: 8px; color: var(--warning);"></i>
                            Last updated: {% if customers %} {{ customers[0].created_at.strftime('%B %d, %Y') if customers[0].created_at else 'Today' }} {% else %} N/A {% endif %}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>
    
    <!-- Add Customer Modal -->
    <div id="addCustomerModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3 class="modal-title"><i class="fas fa-user-plus"></i> Add Customer</h3>
                <button class="close-modal" onclick="closeModal('addCustomerModal')">&times;</button>
            </div>
            
            <form method="POST" action="{{ url_for('add_customer') }}">
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Full Name (Sesotho Name)</label>
                        <input type="text" name="full_name" class="form-control" required placeholder="e.g., Thabo Mokoena">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email</label>
                        <input type="email" name="email" class="form-control" required placeholder="e.g., thabo@email.com">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">Phone Number</label>
                        <input type="tel" name="phone" class="form-control" required placeholder="e.g., +266 123-4567">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Address</label>
                        <input type="text" name="address" class="form-control" required placeholder="e.g., 123 Main Street Maseru">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">ID Number</label>
                        <input type="text" name="id_number" class="form-control" required placeholder="e.g., ID001">
                    </div>
                    <div class="form-group">
                        <label class="form-label">License Number</label>
                        <input type="text" name="license_number" class="form-control" required placeholder="e.g., LIC001">
                    </div>
                </div>
                
                <div class="btn-group">
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Save Customer
                    </button>
                    <button type="button" class="btn btn-clear" onclick="closeModal('addCustomerModal')">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        function showAddCustomerModal() {
            document.getElementById('addCustomerModal').style.display = 'flex';
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
        }
        
        function searchCustomers() {
            const searchText = document.getElementById('customerSearch').value.toLowerCase();
            const rows = document.querySelectorAll('#customerTableBody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchText) ? '' : 'none';
            });
        }
        
        function editCustomer(customerId) {
            alert('Edit customer: ' + customerId + ' (Functionality to be implemented)');
            // Implement edit customer functionality
        }
        
        function deleteCustomer(customerId) {
            if (confirm('Are you sure you want to delete customer ' + customerId + '?')) {
                alert('Delete customer: ' + customerId + ' (Functionality to be implemented)');
                // Implement delete customer functionality
            }
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.style.display = 'none';
            }
        };
        
        // Enable search on Enter key
        document.getElementById('customerSearch').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchCustomers();
            }
        });
    </script>
    {% endblock %}
    '''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', customers_template),
        customers=customers_list,
        active_rentals_count=active_rentals_count
    )

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with app.app_context():
            last_customer = Customer.query.order_by(Customer.id.desc()).first()
            if last_customer:
                last_num = int(last_customer.customer_id[1:])
                new_id = f"C{str(last_num + 1).zfill(3)}"
            else:
                new_id = "C007"
            
            customer = Customer(
                customer_id=new_id,
                full_name=request.form.get('full_name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                address=request.form.get('address'),
                id_number=request.form.get('id_number'),
                license_number=request.form.get('license_number')
            )
            
            db.session.add(customer)
            db.session.commit()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('customers'))
    
    except Exception as e:
        flash(f'Error adding customer: {str(e)}', 'error')
        return redirect(url_for('customers'))

@app.route('/add_random_customer')
def add_random_customer():
    """Add a random customer with Sesotho name"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with app.app_context():
            last_customer = Customer.query.order_by(Customer.id.desc()).first()
            if last_customer:
                last_num = int(last_customer.customer_id[1:])
                new_id = f"C{str(last_num + 1).zfill(3)}"
            else:
                new_id = "C007"
            
            full_name = generate_sesotho_name()
            first_name_lower = full_name.split()[0].lower()
            
            customer = Customer(
                customer_id=new_id,
                full_name=full_name,
                email=f'{first_name_lower}@email.com',
                phone=f'+266 {random.randint(500, 599)}-{random.randint(1000, 9999)}',
                address=f'{random.randint(1, 999)} {random.choice(["Main", "Oak", "Pine", "Maple"])} St {random.choice(["Maseru", "Roma", "Teyateyaneng", "Maputsoe"])}',
                id_number=f'ID{random.randint(1000, 9999)}',
                license_number=f'LIC{random.randint(1000, 9999)}'
            )
            
            db.session.add(customer)
            db.session.commit()
        
        flash(f'Random customer {full_name} added successfully with ID: {new_id}!', 'success')
        return redirect(url_for('customers'))
    
    except Exception as e:
        flash(f'Error adding random customer: {str(e)}', 'error')
        return redirect(url_for('customers'))

@app.route('/add_random_vehicle')
def add_random_vehicle():
    """Add a random vehicle"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with app.app_context():
            last_vehicle = Vehicle.query.order_by(Vehicle.id.desc()).first()
            if last_vehicle:
                last_num = int(last_vehicle.vehicle_id[1:])
                new_id = f"V{str(last_num + 1).zfill(3)}"
            else:
                new_id = "V006"
            
            makes = ['Toyota', 'Honda', 'Ford', 'Nissan', 'Mazda', 'BMW', 'Mercedes', 'Volkswagen']
            models = {
                'Toyota': ['Corolla', 'Camry', 'RAV4', 'Hilux', 'Fortuner'],
                'Honda': ['Civic', 'Accord', 'CR-V', 'HR-V'],
                'Ford': ['Ranger', 'Everest', 'Focus', 'Fiesta'],
                'Nissan': ['X-Trail', 'Navara', 'Qashqai', 'Micra'],
                'Mazda': ['CX-5', 'CX-3', 'Mazda3', 'Mazda6'],
                'BMW': ['3 Series', '5 Series', 'X3', 'X5'],
                'Mercedes': ['C-Class', 'E-Class', 'GLC', 'GLE'],
                'Volkswagen': ['Polo', 'Golf', 'Tiguan', 'Amarok']
            }
            colors = ['White', 'Black', 'Silver', 'Blue', 'Red', 'Gray', 'Green']
            
            make = random.choice(makes)
            model = random.choice(models[make])
            color = random.choice(colors)
            
            letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            numbers = ''.join(random.choices('0123456789', k=3))
            plate_number = f"{letters}{numbers}"
            
            vehicle = Vehicle(
                vehicle_id=new_id,
                make=make,
                model=model,
                year=random.randint(2018, 2024),
                color=color,
                plate_number=plate_number,
                daily_rate=random.choice([1200, 1500, 1800, 2000, 2500, 3000, 3500]),
                status=random.choice(['Available', 'Available', 'Available', 'Maintenance']),
                fuel_type=random.choice(['Petrol', 'Diesel', 'Hybrid']),
                transmission=random.choice(['Automatic', 'Manual']),
                seats=random.choice([4, 5, 7, 8])
            )
            
            db.session.add(vehicle)
            db.session.commit()
        
        flash(f'Random vehicle {make} {model} added successfully!', 'success')
        return redirect(url_for('vehicles'))
    
    except Exception as e:
        flash(f'Error adding random vehicle: {str(e)}', 'error')
        return redirect(url_for('vehicles'))

@app.route('/payments')
def payments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with app.app_context():
        pending_rentals = Rental.query.filter_by(payment_status='Pending').all()
        payment_history = Payment.query.order_by(Payment.created_at.desc()).limit(10).all()
    
    payments_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn active">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                    </a>
                    <a href="{{ url_for('reports') }}" class="nav-btn">
                        <i class="fas fa-chart-line"></i>
                        <span>Reports</span>
                    </a>
                </div>
                
                <div class="sidebar-footer">
                    <div>© 2024 VEHICLE RENTAL</div>
                    <div>Version 2.0.1</div>
                </div>
            </nav>
            
            <main class="content-area">
                <h1 class="page-title"><i class="fas fa-money-bill-wave"></i> Payment Management</h1>
                
                <div class="table-container">
                    <div class="table-header">
                        <h3 style="color: var(--dark);">Pending Payments</h3>
                    </div>
                    
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Rental ID</th>
                                <th>Customer</th>
                                <th>Vehicle</th>
                                <th>Total Amount</th>
                                <th>Deposit</th>
                                <th>Balance</th>
                                <th>Status</th>
                                <th>Due Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for rental in pending_rentals %}
                            <tr>
                                <td>{{ rental.rental_id }}</td>
                                <td>{{ rental.customer_name }}</td>
                                <td>{{ rental.vehicle_info }}</td>
                                <td>R {{ "%.2f"|format(rental.total_amount) }}</td>
                                <td>R {{ "%.2f"|format(rental.deposit) }}</td>
                                <td>R {{ "%.2f"|format(rental.total_amount - rental.deposit) }}</td>
                                <td><span class="status-badge status-{{ rental.payment_status.lower() }}">{{ rental.payment_status }}</span></td>
                                <td>{{ rental.return_date.strftime('%Y-%m-%d') }}</td>
                                <td>
                                    <div class="action-buttons">
                                        <button class="btn-icon btn-success" onclick="processPayment('{{ rental.rental_id }}')" title="Process Payment">
                                            <i class="fas fa-money-bill-wave"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                <div class="table-container" style="margin-top: 30px;">
                    <div class="table-header">
                        <h3 style="color: var(--dark);">Payment History</h3>
                    </div>
                    
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Payment ID</th>
                                <th>Rental ID</th>
                                <th>Customer</th>
                                <th>Amount</th>
                                <th>Method</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for payment in payment_history %}
                            <tr>
                                <td>{{ payment.payment_id }}</td>
                                <td>{{ payment.rental_id }}</td>
                                <td>{{ payment.customer_name }}</td>
                                <td>R {{ "%.2f"|format(payment.amount) }}</td>
                                <td>{{ payment.payment_method }}</td>
                                <td>{{ payment.payment_date.strftime('%Y-%m-%d') }}</td>
                                <td><span class="status-badge status-{{ payment.status.lower() }}">{{ payment.status }}</span></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    </div>
    
    <script>
        function processPayment(rentalId) {
            if (confirm('Process payment for rental ' + rentalId + '?')) {
                window.location.href = '/process_payment/' + rentalId;
            }
        }
    </script>
    {% endblock %}
    '''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', payments_template),
        pending_rentals=pending_rentals,
        payment_history=payment_history
    )

@app.route('/process_payment/<rental_id>')
def process_payment(rental_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        with app.app_context():
            rental = Rental.query.filter_by(rental_id=rental_id).first()
            if rental:
                last_payment = Payment.query.order_by(Payment.id.desc()).first()
                if last_payment:
                    last_num = int(last_payment.payment_id[2:]) if last_payment.payment_id.startswith('PM') else 0
                    payment_id = f"PM{str(last_num + 1).zfill(4)}"
                else:
                    payment_id = "PM0001"
                
                payment = Payment(
                    payment_id=payment_id,
                    rental_id=rental_id,
                    customer_id=rental.customer_id,
                    customer_name=rental.customer_name,
                    amount=rental.total_amount - rental.deposit,
                    payment_date=datetime.now().date(),
                    payment_method='Cash',
                    status='Completed'
                )
                
                rental.payment_status = 'Paid'
                
                db.session.add(payment)
                db.session.commit()
                
                flash(f'Payment processed successfully! Payment ID: {payment_id}', 'success')
            else:
                flash('Rental not found!', 'error')
    
    except Exception as e:
        flash(f'Error processing payment: {str(e)}', 'error')
    
    return redirect(url_for('payments'))

@app.route('/reports')
def reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    with app.app_context():
        total_vehicles = Vehicle.query.count()
        available_vehicles = Vehicle.query.filter_by(status='Available').count()
        total_customers = Customer.query.count()
        active_customers = Customer.query.filter_by(status='Active').count()
        
        completed_payments = Payment.query.filter_by(status='Completed').all()
        total_revenue = sum([p.amount for p in completed_payments])
        
        total_rentals = Rental.query.count()
        active_rentals = Rental.query.filter_by(rental_status='Active').count()
    
    reports_template = '''
    {% block content %}
    <div class="app-container">
        <header class="header">
            <div class="logo">
                <div class="logo-icon">VRS</div>
                <div class="logo-text">VEHICLE RENTAL SYSTEM</div>
            </div>
            <div class="user-info">
                <div class="user-details">
                    <div class="user-name">{{ session.full_name }}</div>
                    <div class="user-role">{{ session.role|title }}</div>
                </div>
                <div class="user-avatar">{{ session.full_name[0]|upper }}</div>
                <a href="{{ url_for('logout') }}" class="btn-logout">
                    <i class="fas fa-sign-out-alt"></i>
                    Logout
                </a>
            </div>
        </header>
        
        <div class="main-content">
            <nav class="sidebar">
                <div class="sidebar-header">
                    <div class="sidebar-avatar">{{ session.full_name[0]|upper }}</div>
                    <h3 class="sidebar-welcome">Welcome, {{ session.full_name.split(' ')[0] }}</h3>
                    <div class="sidebar-role">{{ session.role|title }}</div>
                </div>
                
                <div class="sidebar-nav">
                    <a href="{{ url_for('dashboard') }}" class="nav-btn">
                        <i class="fas fa-chart-bar"></i>
                        <span>Dashboard</span>
                    </a>
                    <a href="{{ url_for('rent_vehicle') }}" class="nav-btn">
                        <i class="fas fa-car"></i>
                        <span>Rent Vehicle</span>
                    </a>
                    <a href="{{ url_for('payments') }}" class="nav-btn">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Payments</span>
                    </a>
                    <a href="{{ url_for('vehicles') }}" class="nav-btn">
                        <i class="fas fa-car-side"></i>
                        <span>Vehicles</span>
                    </a>
                    <a href="{{ url_for('customers') }}" class="nav-btn">
                        <i class="fas fa-users"></i>
                        <span>Customers</span>
                </a>
                <a href="{{ url_for('reports') }}" class="nav-btn active">
                    <i class="fas fa-chart-line"></i>
                    <span>Reports</span>
                </a>
            </div>
            
            <div class="sidebar-footer">
                <div>© 2024 VEHICLE RENTAL</div>
                <div>Version 2.0.1</div>
            </div>
        </nav>
        
        <main class="content-area">
            <h1 class="page-title"><i class="fas fa-chart-line"></i> Reports & Analytics</h1>
            
            <div class="stats-grid">
                <div class="stat-card" style="border-top-color: var(--primary);">
                    <span class="stat-icon"><i class="fas fa-car"></i></span>
                    <div class="stat-value">{{ total_vehicles }}</div>
                    <div class="stat-label">Total Vehicles</div>
                    <div class="stat-desc">{{ available_vehicles }} Available</div>
                </div>
                
                <div class="stat-card" style="border-top-color: var(--secondary);">
                    <span class="stat-icon"><i class="fas fa-users"></i></span>
                    <div class="stat-value">{{ total_customers }}</div>
                    <div class="stat-label">Total Customers</div>
                    <div class="stat-desc">{{ active_customers }} Active</div>
                </div>
                
                <div class="stat-card" style="border-top-color: var(--success);">
                    <span class="stat-icon"><i class="fas fa-money-bill-wave"></i></span>
                    <div class="stat-value">R {{ "%.2f"|format(total_revenue) }}</div>
                    <div class="stat-label">Total Revenue</div>
                    <div class="stat-desc">{{ completed_payments|length }} Payments</div>
                </div>
                
                <div class="stat-card" style="border-top-color: var(--warning);">
                    <span class="stat-icon"><i class="fas fa-chart-line"></i></span>
                    <div class="stat-value">{{ total_rentals }}</div>
                    <div class="stat-label">Total Rentals</div>
                    <div class="stat-desc">{{ active_rentals }} Active</div>
                </div>
            </div>
            
            <div class="form-container" style="margin-top: 30px;">
                <h3 style="color: var(--dark); margin-bottom: 20px;"><i class="fas fa-filter"></i> Generate Report</h3>
                <form method="POST" action="{{ url_for('generate_rental_report') }}">
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Start Date</label>
                            <input type="date" name="start_date" class="form-control" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">End Date</label>
                            <input type="date" name="end_date" class="form-control" required>
                        </div>
                    </div>
                    
                    <div class="form-row">
                        <div class="form-group">
                            <label class="form-label">Report Type</label>
                            <select name="report_type" class="form-control" required>
                                <option value="rental">Rental Report</option>
                                <option value="revenue">Revenue Report</option>
                                <option value="vehicle">Vehicle Utilization</option>
                                <option value="customer">Customer Activity</option>
                            </select>
                        </div>
                    </div>
                    
                    <div class="btn-group">
                        <button type="submit" class="btn btn-success">
                            <i class="fas fa-download"></i> Generate Report
                        </button>
                        <button type="button" class="btn btn-primary" onclick="printReport()">
                            <i class="fas fa-print"></i> Print Report
                        </button>
                    </div>
                </form>
            </div>
        </main>
    </div>
</div>

<script>
    function printReport() {
        window.print();
    }
    
    // Set default dates (last 30 days)
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    
    document.querySelector('input[name="start_date"]').value = thirtyDaysAgo.toISOString().split('T')[0];
    document.querySelector('input[name="end_date"]').value = today.toISOString().split('T')[0];
</script>
{% endblock %}
'''
    
    return render_template_string(
        BASE_TEMPLATE.replace('{% block content %}{% endblock %}', reports_template),
        total_vehicles=total_vehicles,
        available_vehicles=available_vehicles,
        total_customers=total_customers,
        active_customers=active_customers,
        total_revenue=total_revenue,
        total_rentals=total_rentals,
        active_rentals=active_rentals
    )

@app.route('/generate_rental_report', methods=['POST'])
def generate_rental_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        report_type = request.form.get('report_type')
        
        with app.app_context():
            report_content = f"""VEHICLE RENTAL SYSTEM - REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Period: {start_date} to {end_date}
Report Type: {report_type}
{"="*50}

"""
            
            if report_type == 'rental':
                rentals = Rental.query.filter(
                    Rental.created_at >= start_date,
                    Rental.created_at <= end_date
                ).all()
                
                report_content += "RENTAL REPORT\n"
                report_content += "-"*50 + "\n"
                for rental in rentals:
                    report_content += f"""
Rental ID: {rental.rental_id}
Customer: {rental.customer_name}
Vehicle: {rental.vehicle_info}
Period: {rental.rental_date} to {rental.return_date}
Amount: R {rental.total_amount:.2f}
Status: {rental.rental_status}
{"-"*50}
"""
            
            elif report_type == 'revenue':
                payments = Payment.query.filter(
                    Payment.payment_date >= start_date,
                    Payment.payment_date <= end_date
                ).all()
                
                total = sum([p.amount for p in payments])
                
                report_content += "REVENUE REPORT\n"
                report_content += "-"*50 + "\n"
                report_content += f"Total Revenue: R {total:.2f}\n"
                report_content += f"Number of Payments: {len(payments)}\n\n"
                report_content += "Payment Details:\n"
                for payment in payments:
                    report_content += f"• {payment.payment_date}: R {payment.amount:.2f} - {payment.payment_method}\n"
        
        response = make_response(report_content)
        response.headers['Content-Disposition'] = f'attachment; filename={report_type}_report_{datetime.now().strftime("%Y%m%d")}.txt'
        response.headers['Content-type'] = 'text/plain'
        return response
        
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('reports'))

# Run the application
if __name__ == '__main__':
    # Initialize database with default data
    init_database()
    
    print("=" * 70)
    print("VEHICLE RENTAL MANAGEMENT SYSTEM WITH SESOTHO NAMES")
    print("=" * 70)
    print("System starting...")
    print(f"Access URL: http://localhost:5000")
    print("Admin Login: admin / admin123")
    print("Admin Name: Mpho Lereko (Sesotho Name)")
    print("-" * 70)
    print("HARDCODED CUSTOMERS (SESOTHO NAMES ONLY):")
    
    # Query customers within application context
    with app.app_context():
        customers = Customer.query.all()
        for customer in customers:
            print(f"{customer.customer_id}: {customer.full_name}")
    
    print("-" * 70)
    print("NO ENGLISH NAMES (John Doe, Jane Smith, etc.)")
    print("ALL CUSTOMERS USE AUTHENTIC SESOTHO NAMES")
    print("=" * 70)
    app.run(debug=True, port=5000)