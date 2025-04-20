import os

class Config:
    # your Atlas URI (you can also load this from an env var)
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://nisal:bdOS0cvAcKYRF847@cluster0.ld7c5up.mongodb.net/hotel-management?retryWrites=true&w=majority&tls=true"
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secret-key")
    # optional—tells CORS which headers to allow
    CORS_HEADERS = "Content-Type"
