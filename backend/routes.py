from flask import Blueprint, request, jsonify
from database import connect_db
import joblib
import re
import nltk
import os
from nltk.corpus import stopwords
from datetime import date

# Download stopwords if not available
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# -----------------------------
# Load ML Model
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "saved_model", "model.pkl"))
vectorizer = joblib.load(os.path.join(BASE_DIR, "saved_model", "vectorizer.pkl"))

# -----------------------------
# Blueprint
# -----------------------------
routes = Blueprint("routes", __name__)

# Stopwords
stop_words = set(stopwords.words("english"))

# -----------------------------
# Text Preprocessing
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    words = text.split()

    words = [word for word in words if word not in stop_words]

    return " ".join(words)


# -----------------------------
# Home API
# -----------------------------
@routes.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "Sentiment Analysis API Running Successfully"
    })


# -----------------------------
# Predict Sentiment & Save Review
# -----------------------------
@routes.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    student_name = data["student_name"]
    course_name = data["course_name"]
    trainer_name = data["trainer_name"]
    review = data["review"]

    # Clean Review
    clean_review = clean_text(review)

    # Convert to TF-IDF
    vector = vectorizer.transform([clean_review])

    # Predict Sentiment
    sentiment = model.predict(vector)[0]

    # Save to Database
    connection = connect_db()
    cursor = connection.cursor()

    query = """
    INSERT INTO reviews
    (student_name, course_name, trainer_name, review, sentiment, review_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        student_name,
        course_name,
        trainer_name,
        review,
        sentiment,
        date.today()
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Review Saved Successfully",
        "Predicted Sentiment": sentiment
    })


# -----------------------------
# View All Reviews
# -----------------------------
@routes.route("/reviews", methods=["GET"])
def get_reviews():

    connection = connect_db()

    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM reviews
        ORDER BY review_id DESC
    """)

    reviews = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reviews)