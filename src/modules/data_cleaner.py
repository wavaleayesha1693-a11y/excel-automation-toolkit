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

    def get_missing_value_report(self,dataframe:pd.DataFrame) -> pd.DataFrame:

        """
        Generate a report of missing values in the DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame to analyze.

        Returns:
            pd.DataFrame: Report of missing values per column.  

        Raises:
            Exception: If report generation fails.          
        
        """   
        try:
            missing_report = dataframe.isna().sum().reset_index()
            missing_report.columns = ["Column", "Missing Count"]
            missing_report["Missing_Percentage"] = (
                                        missing_report["Missing Count"] / len(dataframe) * 100)
            
            
            logger.info("Generated missing value report.")

            return missing_report

        except Exception as error:
            logger.error(
                "Failed to generate missing value report: %s",
                error
            )
            raise


    def fill_missing_values(self, dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        Fill missing values based on column data type.

        Args:
            dataframe (pd.DataFrame): DataFrame to clean.
            
        Returns:
            pd.DataFrame: Cleaned DataFrame with missing values filled.  

        Raises:
            Exception: If filling missing values fails.          
        
        """
        try:
           cleaned_dataframe = dataframe.copy()
           missing_before = dataframe.isna().sum().sum()

           for column in cleaned_dataframe.columns:
               if pd.api.types.is_numeric_dtype(cleaned_dataframe[column]):
                cleaned_dataframe[column] = (
                    cleaned_dataframe[column].fillna(0)
                )

               else:
                  cleaned_dataframe[column] = (
                        cleaned_dataframe[column].fillna("Unknown")
                    )

           missing_after = cleaned_dataframe.isna().sum().sum()
           
           logger.info(
                    "Filled %d missing values based on column data types.",
                    missing_before - missing_after
                )
           return cleaned_dataframe

    
        except Exception as error:
            logger.error(
                "Failed to fill missing values: %s",
                error
            )
            raise
    
    
            
        
    