import logging
import pandas as pd

logger = logging.getLogger(__name__)

class DataCleaner:
    """ 
    Cleans data in DataFrames for the Excel Automation Toolkit.
    """

    def __init__(self):
        """
        Initialize the Data Cleaner.
        """
        logger.info("Data Cleaner initialized successfully.")   


    def remove_duplicate_rows(self,dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate rows from the DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame to clean.

        Returns:
            pd.DataFrame: Cleaned DataFrame without duplicate rows.  

        Raises:
            Exception: If duplicate removal fails.          
        
        """   
        try:
            row_count_before = dataframe.shape[0]
            cleaned_dataframe = dataframe.drop_duplicates()
            row_count_after = cleaned_dataframe.shape[0]

            logger.info(
                "Removed %d duplicate rows.",
                row_count_before - row_count_after,
            )

            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to remove duplicate rows: %s",
                error
            )
            raise
