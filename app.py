from flask import Flask, render_template, request, session
from time import sleep

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')

# upload audio sample
@app.route('/uploadFile')
def upload_file():
    session['audio'] = 'an audio sample'
    return {
        "status" : "Generating fingerprint"
    }

# generate fingerprint for uploaded audio sample
@app.route('/generateFingerprint')
def generate_fingerprint():
    sleep(5)
    return {
        "status" : "Searching for matches"
    }

@app.route('/searchDatabase')
def search_database():
    sleep(5)
    return {
        "status" : "Found a match for: "+session['audio']
    }

if __name__ == "__main__":
    print("Server is runnin'")
    app.run(debug=True)