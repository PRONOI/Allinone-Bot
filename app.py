from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask on Render 👋"

# Render needs this: bind to 0.0.0.0 on the port it gives us
if __name__ != "__main__":          # gunicorn imports this file
    pass
else:                               # local debug only
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
  
