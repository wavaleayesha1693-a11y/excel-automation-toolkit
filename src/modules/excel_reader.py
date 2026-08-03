import logging
import pandas as pd

from pathlib import Path


logger = logging.getLogger(__name__)

import logging
from pathlib import Path

import pandas as pd


logger = logging.getLogger(__name__)


class ExcelReader:

    def read_excel(self, file_path: Path) -> pd.DataFrame:
        """
        Read Excel file and return contents as DataFrame.

        Args:
            file_path (Path): Path to Excel file.

        Returns:
            pd.DataFrame: Excel data.

        Raises:
            FileNotFoundError: If file does not exist.
            Exception: For unexpected errors.
        """

        try:

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Excel file not found: {file_path}"
                )

            df = pd.read_excel(file_path)

            logger.info(
                "Excel file read successfully: %s",
                file_path
            )

            return df

        except Exception:
            logger.exception(
                "Error occurred while reading Excel file"
            )
            raise