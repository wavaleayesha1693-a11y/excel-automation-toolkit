import logging

import pandas as pd

logger = logging.getLogger(__name__)

class DataValidator:
    """
    Validates data in DataFrames for the Excel Automation Toolkit.
    """

    def __init__(self):
        """
        Initialize the Data Validator.
        """
        logger.info("Data Validator initialized successfully.")
        

    def validate_required_columns(self,
            dataframe: pd.DataFrame,
            required_columns: list[str]
            ) -> bool:
         
        """
        Validate that all required columns exist.

        Args:
            dataframe (pd.DataFrame):
                DataFrame to validate.

            required_columns (list[str]):
                List of required column names.

        Returns:
            bool:
                True if validation succeeds.

        Raises:
            ValueError:
                If one or more required columns are missing.

        """

        try:
            required = set(required_columns)
            available = set(dataframe.columns.tolist())
            missing = required - available

            if missing:
                logger.error(
                    "Missing required columns: %s",
                    ", ".join(sorted(missing))
                )

                raise ValueError(
                    f"Missing required columns: {', '.join(sorted(missing))}"
                )

            logger.info("All required columns are present.")

            return True

        except Exception as error:
            logger.error(
                "Error validating required columns: %s",
                error
            )
            raise