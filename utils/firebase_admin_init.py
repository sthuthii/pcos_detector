import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

# Use service account key
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
