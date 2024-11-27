from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace these with your actual reCAPTCHA keys
SITE_KEY = "your_actual_site_key"
SECRET_KEY = "your_actual_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the response token from the form
        recaptcha_response = request.form.get("g-recaptcha-response")

        # Verify the token with Google's reCAPTCHA API
        payload = {
            "secret": SECRET_KEY,
            "response": recaptcha_response
        }
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
        result = response.json()

        # Check if reCAPTCHA validation succeeded
        if result.get("success"):
            return render_template("success.html")
        else:
            return render_template("mainPage.html", site_key=SITE_KEY, error="CAPTCHA validation failed. Try again!")

    return render_template("mainPage.html", site_key=SITE_KEY, error=None)

@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)