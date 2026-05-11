"""
File service: validates, saves, and cleans up uploaded Python files.
"""
import os
import uuid
import hashlib
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'.py'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class FileService:

    @staticmethod
    def validate_file(file) -> None:
        """
        Raise ValueError if the file fails any validation check.
        Checks: presence, non-empty filename, extension, size, non-empty content.
        """
        if file is None or file.filename == '':
            raise ValueError('No file selected')

        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f'Only Python (.py) files are allowed. Received: "{ext}"')

        # Measure size without loading into memory twice
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)

        if size == 0:
            raise ValueError('Uploaded file is empty')

        if size > MAX_FILE_SIZE:
            mb = size / (1024 * 1024)
            raise ValueError(f'File size ({mb:.1f} MB) exceeds the 10 MB limit')

    @staticmethod
    def save_file(file, upload_folder: str = 'uploads') -> dict:
        """
        Save the file under a UUID-based name to prevent path traversal.

        Returns metadata dict:
            file_path, original_name, unique_filename, file_hash, file_size
        """
        os.makedirs(upload_folder, exist_ok=True)

        content = file.read()
        file_hash = hashlib.sha256(content).hexdigest()
        file.seek(0)

        original_name = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}.py"
        file_path = os.path.join(upload_folder, unique_filename)

        with open(file_path, 'wb') as f:
            f.write(content)

        return {
            'file_path': file_path,
            'original_name': original_name,
            'unique_filename': unique_filename,
            'file_hash': file_hash,
            'file_size': len(content),
        }

    @staticmethod
    def delete_file(file_path: str) -> None:
        """Delete a file silently; ignore missing files."""
        try:
            if file_path and os.path.isfile(file_path):
                os.remove(file_path)
        except OSError as exc:
            print(f"Warning: could not delete {file_path}: {exc}")
