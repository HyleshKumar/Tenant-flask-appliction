import os
from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'mongodb://localhost/your_database_name'
}
db = MongoEngine(app)

class Tenant(db.Document):
    name = db.StringField(required=True)

class ProjectMetadata(db.Document):
    tenant = db.ReferenceField(Tenant)
    csv_location = db.StringField()
    model_location = db.StringField()
    evaluation_results = db.StringField()

@app.route('/tenants', methods=['POST'])
def create_tenant():
    tenant = Tenant(name='Your Tenant Name')
    tenant.save()
    return jsonify({'message': 'Tenant created successfully'})

@app.route('/metadata', methods=['POST'])
def create_metadata():
    tenant = Tenant.objects.first()  # Assuming only one tenant exists for simplicity

    csv_location = os.getenv('CSV_LOCATION')
    target_column = os.getenv('TARGET_COLUMN')

    # Read CSV data and process it
    data = pd.read_csv(csv_location)
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train the model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    evaluation_results = model.score(X_test, y_test)

    # Save metadata to the database
    metadata = ProjectMetadata(
        tenant=tenant,
        csv_location=csv_location,
        model_location='Your S3 Location',
        evaluation_results=str(evaluation_results)
    )
    metadata.save()

    return jsonify({'message': 'Metadata created successfully'})

@app.route('/metadata', methods=['GET'])
def get_metadata():
    metadata = ProjectMetadata.objects.first()  # Assuming only one metadata record exists for simplicity
    tenant = metadata.tenant
    return jsonify({
        'tenant_name': tenant.name,
        'csv_location': metadata.csv_location,
        'model_location': metadata.model_location,
        'evaluation_results': metadata.evaluation_results
    })

if __name__ == '__main__':
    app.run(debug=True)