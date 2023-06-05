Flask MongoDB Web App
This is a Flask-based web application that utilizes MongoDB for storing metadata associated with a machine learning project. The application consists of two main components: an ML component responsible for processing CSV data and generating a model, and a Flask API that interacts with MongoDB to save and retrieve project metadata.

Requirements
Flask
pandas
sklearn

Installation
Clone the repository:

git clone <repository_url>
Navigate to the project directory:


cd flask-mongodb-web-app
Create a virtual environment:

python3 -m venv venv
Activate the virtual environment:

For Windows:

venv\Scripts\activate
For macOS/Linux:


source venv/bin/activate
Install the required dependencies:

pip install -r requirements.txt
Set the necessary environment variables:

CSV_LOCATION: The location of the local CSV file.
TARGET_COLUMN: The target column to predict on.
Start the Flask development server:

css
Copy code
python main.py
Access the Flask API at http://localhost:5000.

Create a tenant entry by sending a POST request to /tenants endpoint:


POST /tenants
Generate and evaluate a model by sending a POST request to /metadata endpoint:

POST /metadata
