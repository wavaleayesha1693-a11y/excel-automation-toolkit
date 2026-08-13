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

    def strip_whitespace(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Strip leading and trailing whitespace from string columns.

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

        Returns:
            pd.DataFrame:
                Transformed DataFrame with whitespace removed.

        Raises:
            Exception:
                If whitespace removal fails.
        """

        try:
            cleaned_dataframe = dataframe.copy()

            string_columns = (
                cleaned_dataframe
                .select_dtypes(include=["object"])
                .columns
            )

            for column in string_columns:
                cleaned_dataframe[column] = (
                    cleaned_dataframe[column].str.strip()
                )

            logger.info(
                "Whitespace stripped from %d string columns.",
                len(string_columns)
            )

            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to strip whitespace from string columns: %s",
                error
            )
            raise

    def standardize_text(
        self,
        dataframe: pd.DataFrame,
        case: str = "lower"
    ) -> pd.DataFrame:
        """
        Standardize text in string columns.

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

            case (str):
                Case format: "lower", "upper", or "title".

        Returns:
            pd.DataFrame:
                Transformed DataFrame.

        Raises:
            ValueError:
                If an unsupported case option is provided.

            Exception:
                If text standardization fails.
        """

        try:
            valid_cases = {"lower", "upper", "title"}

            if case not in valid_cases:
                raise ValueError(
                    "Invalid case option. "
                    "Choose from 'lower', 'upper', or 'title'."
                )

            cleaned_dataframe = dataframe.copy()

            string_columns = (
                cleaned_dataframe
                .select_dtypes(include=["object"])
                .columns
            )

            for column in string_columns:

                if case == "lower":
                    cleaned_dataframe[column] = (
                        cleaned_dataframe[column].str.lower()
                    )

                elif case == "upper":
                    cleaned_dataframe[column] = (
                        cleaned_dataframe[column].str.upper()
                    )

                elif case == "title":
                    cleaned_dataframe[column] = (
                        cleaned_dataframe[column].str.title()
                    )

            logger.info(
                "Text standardized in %d string columns to %s case.",
                len(string_columns),
                case
            )

            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Failed to standardize text in string columns: %s",
                error
            )
            raise

    def rename_columns(
        self,
        dataframe: pd.DataFrame,
        column_mapping: dict[str, str]
    ) -> pd.DataFrame:
        """
        Rename columns based on a provided mapping.

        Existing columns are renamed.
        Missing columns are skipped and logged as warnings.

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

            column_mapping (dict[str, str]):
                Mapping of old column names to new column names.

        Returns:
            pd.DataFrame:
                DataFrame with renamed columns.

        Raises:
            Exception:
                If column renaming fails.
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

    def convert_data_types(self,dataframe: pd.DataFrame,dtype_mapping: dict[str, str]) -> pd.DataFrame:
        """
        Convert specified DataFrame columns to requested data types.

        Supported types:
            - int
            - float
            - string
            - datetime

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

            dtype_mapping (dict[str, str]):
                Mapping of column names to target data types.

        Returns:
            pd.DataFrame:
                DataFrame with successfully converted data types.

        Raises:
            Exception:
                If an unexpected error occurs during conversion.
        """

        try:
            cleaned_dataframe = dataframe.copy()

            available_columns = set(cleaned_dataframe.columns)

            missing_columns = []
            existing_mapping = {}

            for column, dtype in dtype_mapping.items():

                if column in available_columns:
                    existing_mapping[column] = dtype

                else:
                    missing_columns.append(column)

            if missing_columns:
                logger.warning(
                    "Columns not found and skipped during "
                    "data type conversion: %s",
                    ", ".join(missing_columns)
                )

            conversion_errors = []

            for column, dtype in existing_mapping.items():

                try:
                    if dtype == "int":
                        cleaned_dataframe[column] = pd.to_numeric(
                            cleaned_dataframe[column],
                            errors="raise"
                        ).astype("Int64")

                    elif dtype == "float":
                        cleaned_dataframe[column] = pd.to_numeric(
                            cleaned_dataframe[column],
                            errors="raise"
                        ).astype(float)

                    elif dtype == "string":
                        cleaned_dataframe[column] = (
                            cleaned_dataframe[column].astype("string")
                        )

                    elif dtype == "datetime":
                        cleaned_dataframe[column] = pd.to_datetime(
                            cleaned_dataframe[column],
                            errors="raise"
                        )

                    else:
                        raise ValueError(
                            f"Unsupported data type '{dtype}'. "
                            f"Supported types: int, float, string, datetime."
                        )

                    logger.info(
                        "Column '%s' successfully converted to %s.",
                        column,
                        dtype
                    )

                except Exception as error:

                    conversion_errors.append(
                        f"{column} → {dtype}: {error}"
                    )

                    logger.warning(
                        "Column '%s' could not be converted to %s: %s",
                        column,
                        dtype,
                        error
                    )

                    continue

            if conversion_errors:
                logger.warning(
                    "Data type conversion completed with %d warning(s).",
                    len(conversion_errors)
                )

            else:
                logger.info(
                    "All requested data type conversions completed successfully."
                )

            return cleaned_dataframe

        except Exception as error:
            logger.error(
                "Unexpected error during data type conversion: %s",
                error
            )
            raise

    def transform(
        self,
        dataframe: pd.DataFrame,
        case: str = "lower",
        column_mapping: dict[str, str] | None = None,
        dtype_mapping: dict[str, str] | None = None
    ) -> pd.DataFrame:
        """
        Apply the complete data transformation pipeline.

        Transformation sequence:
            1. Strip whitespace
            2. Standardize text
            3. Rename columns
            4. Convert data types

        Args:
            dataframe (pd.DataFrame):
                DataFrame to transform.

            case (str):
                Text case to use: "lower", "upper", or "title".

            column_mapping (dict[str, str] | None):
                Mapping of old column names to new column names.

            dtype_mapping (dict[str, str] | None):
                Mapping of column names to target data types.

        Returns:
            pd.DataFrame:
                Fully transformed DataFrame.

        Raises:
            Exception:
                If an unexpected error occurs during transformation.
        """

        try:
            transformed_dataframe = dataframe

            # Step 1: Strip whitespace
            transformed_dataframe = self.strip_whitespace(
                transformed_dataframe
            )

            # Step 2: Standardize text
            transformed_dataframe = self.standardize_text(
                transformed_dataframe,
                case=case
            )

            # Step 3: Rename columns
            if column_mapping:
                transformed_dataframe = self.rename_columns(
                    transformed_dataframe,
                    column_mapping
                )

            # Step 4: Convert data types
            if dtype_mapping:
                transformed_dataframe = self.convert_data_types(
                    transformed_dataframe,
                    dtype_mapping
                )

            logger.info(
                "Data transformation pipeline completed successfully."
            )

            return transformed_dataframe

        except Exception as error:
            logger.error(
                "Failed to complete data transformation pipeline: %s",
                error
            )
            raise