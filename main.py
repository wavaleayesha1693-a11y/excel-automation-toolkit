import logging
from pathlib import Path

from src.modules.file_handler import FileHandler
from src.modules.excel_reader import ExcelReader
from src.modules.data_validator import DataValidator
from src.modules.data_cleaner import DataCleaner
from src.modules.data_transformer import DataTransformer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


def main():
    """
    Main entry point for the Excel Automation Toolkit.
    """

    # File path
    file_path = Path(
        r"C:\Users\ADMIN\Downloads\Documents\Ayesha_PythonProjects\Employee_Details.xlsx"
    )

    # Required columns
    required_columns = [
        "Employee_ID",
        "Name",
        "Salary"
    ]

    # Initialize classes
    file_handler = FileHandler()
    excel_reader = ExcelReader()
    data_validator = DataValidator()
    data_cleaner = DataCleaner()
    data_transformer = DataTransformer()

    # Validate file
    file_handler.validate_file_exists(file_path)
    file_handler.validate_file_extension(file_path)

    # Read Excel
    dataframe = excel_reader.read_excel(file_path)

    # Validate DataFrame
    data_validator.validate_required_columns(
        dataframe,
        required_columns
    )

    # remove_duplicate_rows
    cleaned_dataframe = data_cleaner.remove_duplicate_rows(
        dataframe
    )    

    # get missing value report
    missing_value_report = data_cleaner.get_missing_value_report(
        cleaned_dataframe
    )

    # fill_missing_values
    cleaned_dataframe = data_cleaner.fill_missing_values(
        cleaned_dataframe
    )

    # strip whitespace
    transformed_dataframe = data_transformer.strip_whitespace(
    cleaned_dataframe
    )

    # standardize_text
    transformed_dataframe = data_transformer.standardize_text(
        transformed_dataframe
    )

    # print("\nMissing Value Report:\n", missing_value_report)
    # print("\n✅ DataFrame cleaning completed successfully!")
    # print("cleaned dataframe:\n", cleaned_dataframe)
    print("standardized text of the DataFrame:\n",transformed_dataframe)
    


if __name__ == "__main__":
    main()