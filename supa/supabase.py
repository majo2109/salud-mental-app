import os
import uuid
from supabase import create_client
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

# Conexión con Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


async def upload_file_to_supabase(file: UploadFile, folder: str = "uploads"):


    bucket_name = "deportistas-mult"   

    
    content = await file.read()


    extension = os.path.splitext(file.filename)[1].lower()
    unique_name = f"{uuid.uuid4()}{extension}"
    file_path = f"{folder}/{unique_name}"

    # Subir a Supabase Storage
    supabase.storage.from_(bucket_name).upload(
        file_path,
        content
    )

    # URL del archivo público
    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{file_path}"

    return public_url
