import pandas as pd
import re
import nltk
import joblib
import os

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Download stopwords (only if not already available)
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

# Load dataset
data = pd.read_csv("dataset/student_course_reviews.csv")

# Select required columns
data = data[["Review", "Sentiment"]]

# Create stopwords set
stop_words = set(stopwords.words("english"))

# Function to clean text
def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Split into words
    words = text.split()

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    # Join words back into a sentence
    return " ".join(words)

# Apply preprocessing
data["Clean_Review"] = data["Review"].apply(clean_text)

# Convert text into numerical features using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data["Clean_Review"])

# Target variable
y = data["Sentiment"]

# Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create and train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Predict test data
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Create saved_model folder if it doesn't exist
os.makedirs("saved_model", exist_ok=True)

# Save trained model
joblib.dump(model, "saved_model/model.pkl")

# Save TF-IDF vectorizer
joblib.dump(vectorizer, "saved_model/vectorizer.pkl")

print("✅ Model saved successfully!")