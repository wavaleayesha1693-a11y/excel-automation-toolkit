from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    """
    Handles all file-related operations for the Excel Automation Toolkit.
    """

    def __init__(self):
        """
        Initialize the FileHandler.
        """
        logger.info("FileHandler initialized successfully.")

    def validate_file_exists(self, file_path:Path)->bool:
        """
        Check whether the given file exists.

        Args:
            file_path (Path): The path to the file to be checked.

        Returns:
            bool: True if the file exists.

        Raises:    
            FileNotFoundError: If the file does not exist.
        """ 

        if not file_path.exists():
            logger.error("File not found:%s",file_path)
            raise FileNotFoundError(f"File not found:{file_path}")

        logger.info("File validated successfully:%s",file_path)
        return True
