from flask import Flask
from flask_cors import CORS
from routes import routes

app = Flask(__name__)

# Enable CORS
CORS(app)

# Register Blueprint
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)