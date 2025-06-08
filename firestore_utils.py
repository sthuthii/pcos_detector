from utils.firebase_admin_init import db

def save_log(email, data):
    doc_ref = db.collection("users").document(email).collection("logs").document()
    doc_ref.set(data)

def get_logs(email):
    return db.collection("users").document(email).collection("logs").stream()
