import joblib
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords if not available
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# Load model and vectorizer
model = joblib.load("saved_model/model.pkl")
vectorizer = joblib.load("saved_model/vectorizer.pkl")

# Stopwords
stop_words = set(stopwords.words("english"))

# Clean text function
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# User input
review = input("Enter Student Review: ")

# Clean review
clean_review = clean_text(review)

# Convert to TF-IDF
review_vector = vectorizer.transform([clean_review])

# Predict sentiment
prediction = model.predict(review_vector)

print("\nPredicted Sentiment:", prediction[0])