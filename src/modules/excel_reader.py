import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class ExcelReader:
    """
    Handles reading Excel files for the Excel Automation Toolkit.
    """

    def __init__(self): 
        """
        Initialize the ExcelReader. 
        """ 
        logger.info("ExcelReader initialized successfully.")


    def read_excel(self, file_path: Path) -> pd.DataFrame:
        """
        Read Excel file and return contents as DataFrame.

        Args:
            file_path (Path): Path to Excel file.

        Returns:
            pd.DataFrame: Excel data.

        Raises:
            Exception: If the Excel file cannot be read.
        """

        file_path = Path(file_path) # Ensure file_path is a Path object

        try:
            dataframe = pd.read_excel(file_path)

            logger.info(
                "Excel file read successfully: %s",
                file_path
            )

            return dataframe

        except Exception as error:
            logger.error(
                "Failed to read Excel file %s: %s",
                file_path,
                error
            )
            raise