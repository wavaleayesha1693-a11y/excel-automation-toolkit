import logging
from pathlib import Path

from src.modules.file_handler import FileHandler
from src.modules.excel_reader import ExcelReader
from src.modules.data_validator import DataValidator
from src.modules.data_cleaner import DataCleaner
from src.modules.data_transformer import DataTransformer
from src.modules.excel_writer import ExcelWriter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)


def main():
    """
    Main entry point for the Excel Automation Toolkit.
    """

    # --------------------------------------------------
    # 1. File configuration
    # --------------------------------------------------

    file_path = Path(
        r"C:\Users\ADMIN\Downloads\Documents\Ayesha_PythonProjects\Employee_Details.xlsx"
    )

    output_path = Path(
    r"C:\Users\ADMIN\Downloads\Documents\Ayesha_PythonProjects\Employee_Details_cleaned.xlsx"
    )

    report_output_path = Path(
    r"C:\Users\ADMIN\Downloads\Documents\Ayesha_PythonProjects\Employee_Details_missing_report.xlsx"
    )

    # Required columns
    required_columns = [
        "Employee_ID",
        "Name",
        "Salary"
    ]

    # Column renaming configuration
    column_mapping = {
        "Employee_ID": "Emp_ID",
        "Name": "Employee_Name",
        "Salary": "Annual_Salary",
        "Department_Name": "Dept_Name"
    }

    # Data type conversion configuration
    dtype_mapping = {
        "Emp_ID": "int",
        "Annual_Salary": "float",
        "Dept_Name": "string"
    }

    # --------------------------------------------------
    # 2. Initialize modules
    # --------------------------------------------------

    file_handler = FileHandler()
    excel_reader = ExcelReader()
    data_validator = DataValidator()
    data_cleaner = DataCleaner()
    data_transformer = DataTransformer()
    excel_writer = ExcelWriter()

    # --------------------------------------------------
    # 3. Validate file
    # --------------------------------------------------

    file_handler.validate_file_exists(file_path)

    file_handler.validate_file_extension(
        file_path
    )

    # --------------------------------------------------
    # 4. Read Excel file
    # --------------------------------------------------

    dataframe = excel_reader.read_excel(file_path)

    # --------------------------------------------------
    # 5. Validate required columns
    # --------------------------------------------------

    data_validator.validate_required_columns(
        dataframe,
        required_columns
    )

    # --------------------------------------------------
    # 6. Remove duplicate rows
    # --------------------------------------------------

    cleaned_dataframe = data_cleaner.remove_duplicate_rows(
        dataframe
    )

    # --------------------------------------------------
    # 7. Generate missing value report
    # --------------------------------------------------

    missing_value_report = data_cleaner.get_missing_value_report(
        cleaned_dataframe
    )

    # --------------------------------------------------
    # 8. Fill missing values
    # --------------------------------------------------

    cleaned_dataframe = data_cleaner.fill_missing_values(
        cleaned_dataframe
    )

    # --------------------------------------------------
    # 9. Run complete transformation pipeline
    # --------------------------------------------------

    transformed_dataframe = data_transformer.transform(
        cleaned_dataframe,
        case="lower",
        column_mapping=column_mapping,
        dtype_mapping=dtype_mapping
    )

    # --------------------------------------------------
    # 10. Display results
    # --------------------------------------------------

    print("\nMissing Value Report:")
    print(missing_value_report)

    print("\nFinal Transformed DataFrame:")
    print(transformed_dataframe)

    print("\nFinal Data Types:")
    print(transformed_dataframe.dtypes)

    print("\nDataFrame transformation completed successfully!")

    # --------------------------------------------------
    # 11. Write to Excel
    # --------------------------------------------------
    
    excel_writer.write_to_excel(
    transformed_dataframe,
    output_path
    )

    #missing_value_report
    excel_writer.write_to_excel(
    missing_value_report,
    report_output_path
    )
    
if __name__ == "__main__":
    main()