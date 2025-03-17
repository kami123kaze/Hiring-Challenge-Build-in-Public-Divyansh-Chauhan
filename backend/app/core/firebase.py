import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Init Firebase if not already
if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_CREDENTIALS")
    if not cred_path:
        raise ValueError("FIREBASE_CREDENTIALS env var missing")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Firestore DB instance
db = firestore.client()

# Get Firestore collection ref
def get_collection_ref(collection_name: str):
    return db.collection(collection_name)

# Get Firestore doc ref
def get_document_ref(collection_name: str, document_id: str):
    return db.collection(collection_name).document(document_id)

# Verify Firebase token
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None

# Assign role to user
def assign_user_role(uid: str, role: str):
    try:
        # Validate role
        if role not in ["teacher", "student"]:
            raise ValueError("Invalid role. Choose 'teacher' or 'student'.")

        # firestore
        user_ref = get_document_ref("users", uid)
        user_ref.set({"role": role}, merge=True)

        # firebase
        auth.set_custom_user_claims(uid, {"role": role})

        return {"message": f"Role '{role}' assigned to user {uid}"}
    
    except Exception as e:
        print(f"Error assigning role: {e}")
        return {"error": str(e)}
    
    
# Get user role
def get_user_role(uid: str):
    try:
        user_ref = get_document_ref("users", uid)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict().get("role")
        return None
    except Exception as e:
        print(f"Error getting user role: {e}")
        return None
