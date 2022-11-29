from flask import Flask, render_template, make_response, request, session
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
#################################################
## generate fingerprint for uploaded audio sample
@app.route('/generateFingerprint', methods=["POST"])
def generate_fingerprint():
    file = request.files["sample"]
    sleep(5)
    fingerprint = ["hash1", "hash2", "hash3"]
    session["fingerprint"] = fingerprint
    return make_response({
        "success": True
    })

## search databasee for matches
@app.route('/searchDatabase')
def search_database():
    sleep(5)
    return {
        "result" : session["fingerprint"]
    }

if __name__ == "__main__":
    print("Server is runnin'")
    app.run(debug=True)