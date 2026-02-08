import os
import secrets
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers
from phonenumbers import timezone, geocoder, carrier, PhoneNumberType
from opencage.geocoder import OpenCageGeocode
import folium
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    searches = db.relationship('SearchHistory', backref='user', lazy=True)

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200))
    carrier = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    country_code = db.Column(db.String(10))
    line_type = db.Column(db.String(50))
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Create database tables
with app.app_context():
    os.makedirs(os.path.join(Config.basedir, 'database'), exist_ok=True)
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context Processor for Firebase Config
@app.context_processor
def inject_firebase():
    return {
        'firebase_config': {
            'apiKey': app.config.get('FIREBASE_API_KEY'),
            'authDomain': app.config.get('FIREBASE_AUTH_DOMAIN'),
            'projectId': app.config.get('FIREBASE_PROJECT_ID'),
            'storageBucket': app.config.get('FIREBASE_STORAGE_BUCKET'),
            'messagingSenderId': app.config.get('FIREBASE_MESSAGING_SENDER_ID'),
            'appId': app.config.get('FIREBASE_APP_ID'),
            'measurementId': app.config.get('FIREBASE_MEASUREMENT_ID')
        }
    }

# Helper functions
def get_number_type(parsed_number):
    n_type = phonenumbers.number_type(parsed_number)
    if n_type == PhoneNumberType.MOBILE: return "Mobile"
    if n_type == PhoneNumberType.FIXED_LINE: return "Fixed Line"
    if n_type == PhoneNumberType.VOIP: return "VoIP"
    if n_type == PhoneNumberType.TOLL_FREE: return "Toll Free"
    return "Unknown"

def get_phone_info(number):
    try:
        # Default to None for region, but handle common formats
        parsed_number = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            # Try with a default region if it doesn't start with +
            if not number.startswith('+'):
                parsed_number = phonenumbers.parse(number, "US") # Default to US or handle differently
                if not phonenumbers.is_valid_number(parsed_number):
                    return None
            else:
                return None
            
        # Basic Info
        location = geocoder.description_for_number(parsed_number, 'en')
        service_provider = carrier.name_for_number(parsed_number, 'en')
        time_zones = timezone.time_zones_for_number(parsed_number)
        line_type = get_number_type(parsed_number)
        
        # Geocoding
        api_key = app.config.get('OPENCAGE_API_KEY')
        print(f"DEBUG: Geocoding location '{location}' with API key length {len(api_key) if api_key else 0}")
        
        geocoder_api = OpenCageGeocode(api_key)
        results = geocoder_api.geocode(str(location))
        
        lat = lng = country_code = None
        if results and len(results) > 0:
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
            country_code = results[0]['components'].get('country_code', '').upper()
            print(f"DEBUG: Geocoding SUCCESS - Lat: {lat}, Lng: {lng}, Country: {country_code}")
        else:
            print(f"DEBUG: Geocoding returned NO RESULTS for '{location}'")
        
        # Map (Dark Theme for 2026 Model)
        map_html = None
        if lat and lng:
            # ... (omitted for brevity, keep existing map logic)
            # Ensure we return the dictionary even if map generation fails
            pass 

        result_data = {
            'number': phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            'location': location or "Unknown Region",
            'carrier': service_provider or "Private Carrier",
            'timezone': time_zones[0] if time_zones else "UTC",
            'latitude': lat,
            'longitude': lng,
            'country_code': country_code,
            'line_type': line_type,
            'map_html': None, # Placeholder
            'is_valid': True
        }

        if lat and lng:
            myMap = folium.Map(location=[lat, lng], zoom_start=10, tiles='CartoDB positron')
            folium.CircleMarker(location=[lat, lng], radius=50, color='#2563eb', fill=True, fill_color='#2563eb', fill_opacity=0.1).add_to(myMap)
            folium.Marker([lat, lng], popup=f"Location: {location}").add_to(myMap)
            result_data['map_html'] = myMap._repr_html_()

        return result_data
    except Exception as e:
        import traceback
        print(f"CRITICAL Tracking Error: {e}")
        traceback.print_exc()
        return None

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/network-status')
def network_status():
    return render_template('network_status.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Authentication failed: Invalid credentials or clearance level', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash('Username unavailable', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account provisioned successfully', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    history = SearchHistory.query.filter_by(user_id=current_user.id).order_by(SearchHistory.searched_at.desc()).all()
    return render_template('dashboard.html', history=history)

@app.route('/global-awareness')
@login_required
def global_awareness():
    history = SearchHistory.query.filter_by(user_id=current_user.id).all()
    
    # Create a global map showing all history points
    global_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
    
    for record in history:
        if record.latitude and record.longitude:
            folium.CircleMarker(
                location=[record.latitude, record.longitude],
                radius=8,
                color='#2563eb',
                fill=True,
                fill_color='#6366f1',
                fill_opacity=0.6,
                popup=f"Target: {record.phone_number}<br>Loc: {record.location}"
            ).add_to(global_map)
            
    map_html = global_map._repr_html_()
    return render_template('global_awareness.html', map_html=map_html)

@app.route('/track', methods=['POST'])
@login_required
def track():
    number = request.form.get('phone_number')
    if not number:
        return jsonify({'error': 'Terminal input required'}), 400
    
    try:
        phone_info = get_phone_info(number)
        if phone_info:
            search_record = SearchHistory(
                phone_number=phone_info['number'],
                location=phone_info['location'],
                carrier=phone_info['carrier'],
                latitude=phone_info['latitude'],
                longitude=phone_info['longitude'],
                country_code=phone_info['country_code'],
                line_type=phone_info['line_type'],
                user_id=current_user.id
            )
            db.session.add(search_record)
            db.session.commit()
            return jsonify(phone_info)
        else:
            return jsonify({'error': 'Geospatial resolution returned no data for this identifier.'}), 404
    except Exception as e:
        db.session.rollback()
        print(f"ERROR in /track route: {e}")
        return jsonify({'error': f'Uplink Error: {str(e)}'}), 500

@app.route('/delete-history/<int:record_id>', methods=['POST'])
@login_required
def delete_history(record_id):
    record = SearchHistory.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access to protocol logs'}), 403
    
    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/history-details/<int:record_id>')
@login_required
def history_details(record_id):
    record = SearchHistory.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'phone_number': record.phone_number,
        'location': record.location,
        'carrier': record.carrier,
        'latitude': record.latitude,
        'longitude': record.longitude,
        'country_code': record.country_code,
        'line_type': record.line_type,
        'searched_at': record.searched_at.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/record-info/<int:record_id>')
@login_required
def record_info(record_id):
    record = SearchHistory.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        flash("Unauthorized access to restricted intelligence packets.", "danger")
        return redirect(url_for('dashboard'))
    return render_template('record_info.html', record=record)

@app.route('/api/validate-number', methods=['POST'])
def validate_number():
    number = request.json.get('number')
    try:
        parsed = phonenumbers.parse(number)
        return jsonify({'valid': phonenumbers.is_valid_number(parsed)})
    except:
        return jsonify({'valid': False})

if __name__ == '__main__':
    app.run(debug=True, port=8000)