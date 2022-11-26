from flask import Flask, render_template, request, session
from time import sleep
from parameters import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# View Routers
## home page
@app.route('/')
def index():
    return render_template('index.html')


# API Routers
## upload audio sample
@app.route('/uploadFile', methods=["POST"])
def upload_file():
    file = request.files["sample"]
    
    return {
        "status" : "Generating fingerprint"
    }

## generate fingerprint for uploaded audio sample
@app.route('/generateFingerprint')
def generate_fingerprint():
    sleep(5)
    return {
        "status" : "Searching for matches"
    }

## search databasee for matches
@app.route('/searchDatabase')
def search_database():
    sleep(5)
    return {
        "status" : "Found a match for: "+session['audio']
    }

if __name__ == "__main__":
    print("Server is runnin'")
    app.run(debug=True)