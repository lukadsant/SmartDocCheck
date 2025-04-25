import os
from fastapi import UploadFile
from uuid import uuid4

async def save_upload_file(file: UploadFile, destination_folder: str) -> str:
    os.makedirs(destination_folder, exist_ok=True)
    filename = f"{uuid4().hex}_{file.filename}"
    filepath = os.path.join(destination_folder, filename)

    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return filepath
