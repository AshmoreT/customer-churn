import datetime
import json
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
    # Relationship with predictions
    predictions = db.relationship('Prediction', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Prediction(db.Model):
    """Model for storing prediction history"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    file_name = db.Column(db.String(128), nullable=False)
    total_customers = db.Column(db.Integer, nullable=False)
    churn_count = db.Column(db.Integer, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    precision = db.Column(db.Float, nullable=False)
    recall = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    
    # Store prediction details as JSON
    prediction_details = db.Column(db.Text, nullable=False)
    feature_importance = db.Column(db.Text, nullable=False)
    
    def get_details(self):
        """Return prediction details as a dictionary with error handling"""
        try:
            details = json.loads(self.prediction_details)
            
            # Ensure customer_predictions is a dict and has proper structure
            if 'customer_predictions' not in details or not isinstance(details['customer_predictions'], dict):
                details['customer_predictions'] = {}
                
            # Ensure each customer prediction item has the expected structure and required fields
            for customer_id, prediction_data in details['customer_predictions'].items():
                # Check if prediction_data is a dictionary
                if not isinstance(prediction_data, dict):
                    # If not a dict, create a new default dict
                    details['customer_predictions'][customer_id] = {
                        'prediction': 0,
                        'churn_probability': 0.0,
                        'Customer_ID': f"CUST{customer_id}"
                    }
                else:
                    # Make sure required fields exist in the dict
                    if 'prediction' not in prediction_data:
                        prediction_data['prediction'] = 0
                    
                    if 'churn_probability' not in prediction_data:
                        prediction_data['churn_probability'] = 0.0
            
            return details
        except Exception as e:
            print(f"Error parsing prediction details: {str(e)}")
            return {'customer_predictions': {}, 'confusion_matrix': None}
    
    def get_feature_importance(self):
        """Return feature importance as a dictionary with error handling"""
        try:
            return json.loads(self.feature_importance)
        except Exception as e:
            print(f"Error parsing feature importance: {str(e)}")
            return {'features': ['Feature 1', 'Feature 2', 'Feature 3'], 
                   'importance': [0.5, 0.3, 0.2]}
    
    def __repr__(self):
        return f'<Prediction {self.id}: {self.file_name}>'
