from fastapi import UploadFile


async def validate_upload_file(upload_file: UploadFile) -> bool:
    file_bytes = await upload_file.read()
    file_content = file_bytes.decode()
    return "metadata" in file_content
