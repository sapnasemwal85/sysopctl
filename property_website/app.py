from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Property model
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('properties'))
        return 'Invalid credentials'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/properties')
def properties():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('properties.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    properties = Property.query.all()
    properties_list = [{'id': prop.id, 'name': prop.name, 'price': prop.price} for prop in properties]
    return jsonify(properties_list)

if __name__ == '__main__':
    db.create_all()  # Create database tables
    # Add some dummy properties for testing
    if not Property.query.first():
        db.session.add(Property(name='Luxury Villa', price=1000000))
        db.session.add(Property(name='Urban Apartment', price=500000))
        db.session.commit()
    app.run(debug=True)
