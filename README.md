# Pulsed Workshop sample web application

Thrown together quickly using Flask.

## Flask App

This web application is made using Flask, an HTTP API framework that helps with setting up
web applications extremely fast. I don't usually code in Python, especially for web
development, so this is definitely not amazing.

Below you can see how to install this app and run it, feel free to make some modifications!

### Installation

1. **Clone the repository:**
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a virtual environment:**
   ```sh
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```

4. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Running the App

1. **Set the Flask app environment variable:**
   ```sh
   export FLASK_APP=main.py
   ```

2. **Run the Flask app:**
   ```sh
   flask run
   ```

3. **Access the app in your web browser:**
   Open your web browser and go to `http://127.0.0.1:5000/`.