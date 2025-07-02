import os
from pathlib import Path

from cache import StandardViewCacheFile
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

    def validate_file(self, session_id: str, cache_file: StandardViewCacheFile) -> tuple[bool, str]:
        try:
            temp_file = os.path.join(self.lattice_directory, cache_file.filename)
            with open(temp_file, "wb") as file:
                file.write(cache_file.content)
                self.logger.debug(session_id, f"Created temp file {cache_file.filename}")

            self.lattice.validate_file(temp_file)

            is_valid = True
            validation_messages = f"Validation successful for {cache_file.filename}"
        except Exception as exception:
            is_valid = False
            validation_messages = str(exception)
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)
                self.logger.debug(session_id, f"Removed temp file {cache_file.filename}")

        self.logger.debug(session_id, validation_messages)
        return is_valid, validation_messages
