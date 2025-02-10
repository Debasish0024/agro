from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd 
import joblib
import os


app = Flask(__name__)

# Configure PostgreSQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Deba%401234@localhost/agriprophets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


model_path = os.path.join(os.path.dirname(__file__), 'models', 'potato_model.pkl')
potato_model = joblib.load(model_path)

class Users(db.Model):
    username = db.Column(db.String(50), primary_key=True)  # Primary key provided by the user
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Prediction(db.Model):
    prediction_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('users.username'), nullable=False)  # Foreign key to the users table
    crop_name = db.Column(db.String(100), nullable=False)
    fertilizer_price = db.Column(db.Numeric(10, 2), nullable=False)
    petrol_price = db.Column(db.Numeric(10, 2), nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)
    temperature = db.Column(db.Numeric(5, 2), nullable=False)
    rainfall = db.Column(db.Numeric(5, 2), nullable=False)
    predicted_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Report(db.Model):
    report_id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction.prediction_id'), nullable=False)  # Foreign key to predictions
    actual_price = db.Column(db.Numeric(10, 2), nullable=False)
    reported_at = db.Column(db.DateTime, default=db.func.current_timestamp())


with app.app_context():
    db.create_all()

# Define HTML Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/report')
def report():
    return render_template('report.html')

# Define API Routes
@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print(data)

        existing_user = Users.query.filter((Users.username == data['username']) | (Users.email == data['email'])).first()
        if existing_user:
            return jsonify({'message': 'Username or email already exists!'}), 409

        hashed_password = generate_password_hash(data['password'])

        new_user = Users(
            username=data['username'],
            name=data['name'],
            location=data['location'],
            email=data['email'],
            phone=data['phone'],
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Internal server error!'}), 500


@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = Users.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

@app.route('/predict', methods=['POST'])
def predict_price():
    data = request.get_json()

    
    username = data.get('username', 'anonymous')  # Use 'anonymous' or similar default if not provided
    
    # Fetch temperature and rainfall data (Ensure these functions are implemented)
    temperature = fetch_temperature_data()  # Replace with actual implementation
    rainfall = fetch_rainfall_data()        # Replace with actual implementation

    data['ds'] = pd.to_datetime(f"{data['Year']}-{data['Month']}-{data['Day']}")
    
    
    # Check that temperature and rainfall data are valid
    if temperature is None or rainfall is None:
        return jsonify({'message': 'Failed to fetch weather data.'}), 500
    input_data = pd.DataFrame({
        'ds': [data['ds']],
        'Fertilizer': [data['fertilizer_price']],
        'Petrol Price': [data['petrol_price']],
        'District Name': [data['district_name']],
        'Lag_Price': [data['lag_price']],
        'Rainfall': [data['rainfall']]
    })
    predicted_price = potato_model.predict(input_data)[0]
    
    new_prediction = Prediction(
        username=username,  # Adjust as needed if no login required
        crop_name=data['crop_name'],
        fertilizer_price=data['fertilizer_price'],
        petrol_price=data['petrol_price'],
        prediction_date=data['ds'],
        temperature=temperature,
        rainfall=rainfall,
        predicted_price=predicted_price
    )

    db.session.add(new_prediction)
    db.session.commit()

    return jsonify({'message': 'Prediction submitted successfully!', 'prediction_id': new_prediction.prediction_id}), 201



@app.route('/result/<int:prediction_id>', methods=['GET'])
def result(prediction_id):
    prediction = Prediction.query.get(prediction_id)

    if prediction:
        return jsonify({
            'prediction_id': prediction.prediction_id,
            'crop_name': prediction.crop_name,
            'predicted_price': prediction.predicted_price
        }), 200
    else:
        return jsonify({'message': 'Prediction not found!'}), 404

@app.route('/report', methods=['POST'])
def report_price():
    data = request.get_json()
    prediction = Prediction.query.get(data['prediction_id'])

    if not prediction:
        return jsonify({'message': 'Prediction not found!'}), 404

    actual_price = ActualPrice(
        prediction_id=data['prediction_id'],
        actual_price=data['actual_price']
    )

    db.session.add(actual_price)
    db.session.commit()

    return jsonify({'message': 'Report submitted successfully!'}), 201

if __name__ == "__main__":
    app.run(debug=True)


def fetch_temperature_data():
    
    return 25.0  # Example temperature value

def fetch_rainfall_data():
    
    return 150.0  # Example rainfall value
