import logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class ExcelWriter:
    """
    Handles writing DataFrames to Excel files
    for the Excel Automation Toolkit.
    """
    def __init__(self):
        """
        Initialize the ExcelWriter.
        """
        logger.info("ExcelWriter initialized successfully.")

    def write_to_excel(self, dataframe: pd.DataFrame, output_path: Path) -> None:
        """
        Write the DataFrame to an Excel file.

        Args:
            dataframe (pd.DataFrame): DataFrame to write.
            output_path (Path): Path to the output Excel file.

        Raises:
            Exception: If writing to Excel fails.
        """
        try:
            # Ensure output_path is a Path object
            output_path = Path(output_path)

            # Create output directory if it does not exist
            if not output_path.parent.exists():
                output_path.parent.mkdir(
                    parents=True,
                    exist_ok=True
                )

                logger.info(
                    "Created output directory: %s",
                    output_path.parent
                )

            # Prevent accidental overwrite
            if output_path.exists():
                logger.error(
                    "Output file already exists: %s",
                    output_path
                )

                raise FileExistsError(
                    f"Output file already exists: {output_path}"
                )

            # Write DataFrame
            dataframe.to_excel(
                output_path,
                index=False
            )

            logger.info(
                "DataFrame written to Excel successfully: %s",
                output_path
            )

        except FileExistsError:
            raise

        except Exception as error:
            logger.error(
                "Failed to write DataFrame to Excel: %s",
                error
            )
            raise