import pandas as pd
import pytest

from src.modules.excel_reader import ExcelReader


def test_read_excel(tmp_path):
    """
    Test that an Excel file is successfully read
    into a DataFrame.
    """

    test_file = tmp_path / "test.xlsx"

    test_dataframe = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Salary": [50000, 60000]
    })

    test_dataframe.to_excel(test_file, index=False)

    excel_reader = ExcelReader()

    result = excel_reader.read_excel(test_file)

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)
    assert list(result.columns) == ["Name", "Salary"]


def test_read_invalid_excel_file(tmp_path):
    """
    Test that reading an invalid Excel file raises an exception.
    """

    test_file = tmp_path / "invalid.xlsx"
    test_file.write_text("This is not an Excel file.")

    excel_reader = ExcelReader()

    with pytest.raises(Exception):
        excel_reader.read_excel(test_file)