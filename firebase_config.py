import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded service account key
cred = credentials.Certificate("demo01-15564-firebase-adminsdk-fbsvc-0f811dddd9.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

firebase_config = {
    "apiKey": "AIzaSyAYVd_88XdAwGGbclcp_RZ1LhuWTc4b-5U",
    "authDomain": "demo02-e0c66.firebaseapp.com",
    "projectId": "demo02-e0c66",
    "databaseURL": "https://demo02-e0c66-default-rtdb.firebaseio.com",
    "storageBucket": "demo02-e0c66.firebasestorage.app",
    "messagingSenderId": "1090057688003",
    "appId": "1:1090057688003:web:7e44f034b6446b99646376"
}

