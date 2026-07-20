import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="santhiya@123",
        database="sentiment_analysis"
    )
    return connection