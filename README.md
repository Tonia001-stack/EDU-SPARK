Edu-Spark: Your Daily Micro-Learning Platform
A project created by Anthonia Othetheso.

Features
User Authentication: Secure user registration and login with password hashing using bcrypt.

Secure Sessions: Flask session management with a secret key loaded from an environment file for enhanced security.

Content Delivery: Serve both free and premium content dynamically from a MySQL database.

Paystack Integration: A full payment flow that initiates and verifies real transactions.

Responsive Design: A clean, mobile-friendly user interface.

Technology Stack
Backend: Python 3, Flask

Database: MySQL

Payment Gateway: Paystack API

Frontend: HTML, CSS, JavaScript

Dependencies: Flask, Flask-MySQLdb, bcrypt, requests, python-dotenv

Setup and Installation
Follow these steps to get the project up and running on your local machine.

Step 1: Clone the Repository
Clone this repository to your local machine using the following command:

git clone <your-repository-url>
cd Edu-Spark


Step 2: Create a Virtual Environment
It is highly recommended to use a virtual environment to manage project dependencies.

python3 -m venv .venv


Activate the virtual environment:

macOS / Linux:

source .venv/bin/activate


Windows:

.venv\Scripts\activate


Step 3: Install Dependencies
With your virtual environment activated, install the required Python packages from the requirements.txt file.

pip install -r requirements.txt


Step 4: Database Setup
Ensure you have MySQL installed and running.

Open your MySQL client and run the commands in the schema.sql file to create the eduspark database and its tables.

# Inside your MySQL client
SOURCE /path/to/your/project/schema.sql;


Step 5: Configure Environment Variables
Create a file named .env in the root directory of your project (the same folder as app.py). This file will store your sensitive API keys and a secret key.

Replace the placeholder values with your actual keys from Paystack.

PAYSTACK_SECRET_KEY=sk_test_...
PAYSTACK_PUBLIC_KEY=pk_test_...
FLASK_SECRET_KEY=e5022a17a233e3cbae08ea1e2ad711ba


Step 6: Run the Application
Now you can start the Flask development server.

python app.py


Your application should now be running! Open your web browser and navigate to http://127.0.0.1:5000 to start using Edu-Spark.

Created By
Anthonia Othetheso.# EDU-SPARK
