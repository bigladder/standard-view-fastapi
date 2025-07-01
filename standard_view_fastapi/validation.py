import os
from pathlib import Path

from fastapi import UploadFile
from lattice import Lattice
from logger import StandardViewLogger
from settings import StandardViewSettings


class StandardViewValidator:
    def __init__(self, settings: StandardViewSettings, logger: StandardViewLogger) -> None:
        self.lattice_directory: str = os.path.join(Path.cwd(), settings.lattice_directory)
        os.makedirs(self.lattice_directory, exist_ok=True)
        self.lattice: Lattice = Lattice(
            root_directory=settings.schema_directory,
            build_directory=self.lattice_directory,
            build_output_directory_name=None,
            build_validation=True,
        )
        self.logger: StandardViewLogger = logger

    async def validate_file(self, session_id: str, upload_file: UploadFile) -> tuple[bool, str]:
        try:
            file_name = upload_file.filename or f"{session_id}.json"
            temp_file = os.path.join(self.lattice_directory, file_name)
            file_bytes = await upload_file.read()
            with open(temp_file, "wb") as file:
                file.write(file_bytes)
                self.logger.debug(session_id, f"Created temp file {file_name}")

            self.lattice.validate_file(temp_file)

            is_valid = True
            validation_messages = f"Validation successful for {file_name}"
        except Exception as exception:
            is_valid = False
            validation_messages = str(exception)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                self.logger.debug(session_id, f"Removed temp file {file_name}")

        self.logger.debug(session_id, validation_messages)
        return is_valid, validation_messages
