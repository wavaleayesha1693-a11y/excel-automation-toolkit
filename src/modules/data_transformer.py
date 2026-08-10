import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    """
    Performs data transformations for the Excel Automation Toolkit.
    """

    def __init__(self):
        """
        Initialize the Data Transformer.
        """
        logger.info("Data Transformer initialized successfully.") 

    def strip_whitespace(self,dataframe:pd.DataFrame) -> pd.DataFrame:
        """
        Strip leading and trailing whitespace from string columns in the DataFrame.

        Args:
            dataframe (pd.DataFrame): DataFrame to transform.

        Returns:
            pd.DataFrame: Transformed DataFrame with whitespace stripped from string columns.

        Raises:
        Exception:
            If whitespace removal fails.

        """        

        try:
            cleaned_dataframe = dataframe.copy()
            string_columns = cleaned_dataframe.select_dtypes(include=["object"]).columns
            for column in string_columns:
                cleaned_dataframe[column] = cleaned_dataframe[column].str.strip()

            logger.info("Whitespace stripped from %d string columns.",
                        len(string_columns))
            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to strip whitespace from string columns: %s", 
                 error
                )
            raise

    def standardize_text(self,dataframe:pd.DataFrame,case:str = 'lower') -> pd.DataFrame:
        """
        Standardize text in string columns to a consistent format (e.g., title case).

        Args:
            dataframe (pd.DataFrame): DataFrame to transform.
            case (str):
                Case format: "lower", "upper", or "title".

        Returns:
            pd.DataFrame: Transformed DataFrame with standardized text in string columns.

        Raises:
        Exception: If text standardization fails.

        """    
        
        try:
            valid_cases = ['lower', 'upper', 'title']
            if case not in valid_cases:
                raise ValueError(f"Invalid case option. Choose from {valid_cases}.")
            
            cleaned_dataframe = dataframe.copy()
            string_columns = cleaned_dataframe.select_dtypes(include=["object"]).columns

            for column in string_columns:
                if case == 'lower':
                    cleaned_dataframe[column] = cleaned_dataframe[column].str.lower()
                elif case == 'upper':
                    cleaned_dataframe[column] = cleaned_dataframe[column].str.upper()
                elif case == 'title':
                    cleaned_dataframe[column] = cleaned_dataframe[column].str.title()
                
            logger.info("Text standardized in %d string columns to %s case.",
                        len(string_columns), case)
            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to standardize text in string columns: %s", 
                 error
                )
            raise
        

    def rename_columns(self,dataframe: pd.DataFrame,column_mapping: dict[str, str]) -> pd.DataFrame:

        """
        Rename columns in the DataFrame based on a provided mapping.

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

            column_mapping (dict[str, str]):
                Dictionary mapping existing column names
                to new column names.

        Returns:
            pd.DataFrame:
                Transformed DataFrame with renamed columns.

        Raises:
            Warning:
                If some columns in the mapping are not found in the DataFrame.
            ValueError:
                If renaming of columnns fails
        """
        try:
            cleaned_dataframe = dataframe.copy()

            available_columns = set(cleaned_dataframe.columns)

            existing_mapping = {}
            missing_columns = []

            for old_column, new_column in column_mapping.items():

                if old_column in available_columns:
                    existing_mapping[old_column] = new_column
                else:
                    missing_columns.append(old_column)

            if missing_columns:
                logger.warning(
                    "Columns not found and skipped: %s",
                    ", ".join(missing_columns)
                )

            if existing_mapping:
                cleaned_dataframe = cleaned_dataframe.rename(
                    columns=existing_mapping
                )

                logger.info(
                    "Successfully renamed %d columns.",
                    len(existing_mapping)
                )

            else:
                logger.warning(
                    "No columns from the provided mapping were found."
                )

            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to rename columns in the DataFrame: %s",
                error
            )
            raise