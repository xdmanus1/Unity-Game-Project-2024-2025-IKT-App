import os
import sys
from supabase import create_client, Client, AuthApiError
import uuid
import getpass
from datetime import datetime

# Replace with your Supabase project URL and API key
SUPABASE_URL = "https://jdisuejxelaxgsjsctvm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImpkaXN1ZWp4ZWxheGdzanNjdHZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjc2NDIzOTEsImV4cCI6MjA0MzIxODM5MX0.V07FjL6CLUO7_Hz2LoK4w3L75iIm4dbpCaWEu32mRo0"


def authenticate_user(email: str, password: str) -> Client:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        # Authenticate the user
        user = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        print(f"Authenticated user {email}")
        return supabase
    except AuthApiError as e:
        print(f"Authentication failed: {str(e)}")
        sys.exit(1)


def upload_bat_file(supabase: Client, file_path: str) -> bool:
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return False

    try:
        # Generate a unique filename
        file_name = f"{uuid.uuid4()}.bat"

        # Upload file to Supabase Storage
        with open(file_path, "rb") as file:
            supabase.storage.from_("game-updates").upload(
                file=file,
                path=file_name,
                file_options={"content-type": "application/x-bat"},
            )

        # Insert record into the database
        current_time = datetime.utcnow().isoformat()  # Current timestamp
        supabase.table("bat_files").insert(
            {
                "file_path": file_name,
                "created_at": current_time,  # Explicitly set created_at if not auto-handled
            }
        ).execute()

        print(f"Successfully uploaded {file_path} to Supabase.")
        return True
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python uploader.py <path_to_bat_file>")
        sys.exit(1)

    bat_file_path = sys.argv[1]

    # Get email and password from user input
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")

    # Authenticate the user
    supabase = authenticate_user(email, password)

    # Upload the .bat file after authentication
    upload_bat_file(supabase, bat_file_path)
