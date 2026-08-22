from pathlib import Path

import pandas as pd

from src.modules.file_handler import FileHandler
from src.modules.excel_reader import ExcelReader
from src.modules.data_validator import DataValidator
from src.modules.data_cleaner import DataCleaner
from src.modules.data_transformer import DataTransformer
from src.modules.excel_writer import ExcelWriter


def test_complete_excel_automation_pipeline(tmp_path):
    """
    Test the complete Excel Automation Toolkit pipeline
    from input Excel file to generated output files.
    """

    # --------------------------------------------------
    # 1. Create test input Excel file
    # --------------------------------------------------

    input_path = tmp_path / "Employee_Details.xlsx"

    input_dataframe = pd.DataFrame({
        "Employee_ID": [1, 2, 2, 3],
        "Name": [" Alice ", " Bob ", " Bob ", None],
        "Salary": [50000, 60000, 60000, None],
        "Department": [" IT ", " HR ", " HR ", " Finance "]
    })

    input_dataframe.to_excel(
        input_path,
        index=False
    )

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
    # 3. Validate input file
    # --------------------------------------------------

    assert file_handler.validate_file_exists(input_path) is True

    # --------------------------------------------------
    # 4. Read Excel
    # --------------------------------------------------

    dataframe = excel_reader.read_excel(input_path)

    assert not dataframe.empty

    # --------------------------------------------------
    # 5. Validate required columns
    # --------------------------------------------------

    required_columns = [
        "Employee_ID",
        "Name",
        "Salary"
    ]

    assert data_validator.validate_required_columns(
        dataframe,
        required_columns
    ) is True

    # --------------------------------------------------
    # 6. Remove duplicates
    # --------------------------------------------------

    cleaned_dataframe = data_cleaner.remove_duplicate_rows(
        dataframe
    )

    assert len(cleaned_dataframe) == 3

    # --------------------------------------------------
    # 7. Generate missing-value report
    # --------------------------------------------------

    missing_value_report = (
        data_cleaner.get_missing_value_report(
            cleaned_dataframe
        )
    )

    assert not missing_value_report.empty

    # --------------------------------------------------
    # 8. Fill missing values
    # --------------------------------------------------

    cleaned_dataframe = data_cleaner.fill_missing_values(
        cleaned_dataframe
    )

    assert cleaned_dataframe.isna().sum().sum() == 0

    # --------------------------------------------------
    # 9. Transform DataFrame
    # --------------------------------------------------

    transformed_dataframe = data_transformer.transform(
        cleaned_dataframe,
        case="lower",
        column_mapping={
            "Employee_ID": "Emp_ID",
            "Name": "Employee_Name",
            "Salary": "Annual_Salary"
        },
        dtype_mapping={
            "Emp_ID": "int",
            "Annual_Salary": "float",
            "Employee_Name": "string"
        }
    )

    # --------------------------------------------------
    # 10. Verify transformation
    # --------------------------------------------------

    assert "Emp_ID" in transformed_dataframe.columns
    assert "Employee_Name" in transformed_dataframe.columns
    assert "Annual_Salary" in transformed_dataframe.columns

    assert "Employee_ID" not in transformed_dataframe.columns
    assert "Name" not in transformed_dataframe.columns
    assert "Salary" not in transformed_dataframe.columns

    assert str(
        transformed_dataframe["Emp_ID"].dtype
    ) == "Int64"

    assert (
        transformed_dataframe["Annual_Salary"].dtype
        == float
    )

    assert (
        str(transformed_dataframe["Employee_Name"].dtype)
        == "string"
    )

    # --------------------------------------------------
    # 11. Create output paths
    # --------------------------------------------------

    output_directory = tmp_path / "output"

    cleaned_output_path = (
        output_directory
        / f"{input_path.stem}_cleaned{input_path.suffix}"
    )

    report_output_path = (
        output_directory
        / f"{input_path.stem}_missing_report{input_path.suffix}"
    )

    # --------------------------------------------------
    # 12. Write cleaned Excel
    # --------------------------------------------------

    excel_writer.write_to_excel(
        transformed_dataframe,
        cleaned_output_path
    )

    # --------------------------------------------------
    # 13. Write missing-value report
    # --------------------------------------------------

    excel_writer.write_to_excel(
        missing_value_report,
        report_output_path
    )

    # --------------------------------------------------
    # 14. Verify output files
    # --------------------------------------------------

    assert cleaned_output_path.exists()
    assert report_output_path.exists()

    # --------------------------------------------------
    # 15. Verify generated Excel content
    # --------------------------------------------------

    generated_dataframe = pd.read_excel(
        cleaned_output_path
    )

    generated_report = pd.read_excel(
        report_output_path
    )

    assert not generated_dataframe.empty
    assert not generated_report.empty

    assert list(generated_dataframe.columns) == [
        "Emp_ID",
        "Employee_Name",
        "Annual_Salary",
        "Department"
    ]