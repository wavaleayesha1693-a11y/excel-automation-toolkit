import pandas as pd
import pytest

from src.modules.excel_writer import ExcelWriter


def test_write_to_excel(tmp_path):
    """
    Test that a DataFrame is successfully written to Excel.
    """

    output_path = tmp_path / "output" / "result.xlsx"

    dataframe = pd.DataFrame({
        "Name": ["Alice", "Bob"],
        "Salary": [50000, 60000]
    })

    writer = ExcelWriter()

    writer.write_to_excel(
        dataframe,
        output_path
    )

    assert output_path.exists()

    result = pd.read_excel(output_path)

    assert result.shape == (2, 2)
    assert result["Name"].tolist() == ["Alice", "Bob"]
    assert result["Salary"].tolist() == [50000, 60000]


def test_output_directory_created(tmp_path):
    """
    Test that the output directory is created automatically.
    """

    output_path = (
        tmp_path
        / "new_output"
        / "nested"
        / "result.xlsx"
    )

    dataframe = pd.DataFrame({
        "Name": ["Alice"]
    })

    writer = ExcelWriter()

    writer.write_to_excel(
        dataframe,
        output_path
    )

    assert output_path.exists()
    assert output_path.parent.exists()


def test_existing_output_file_raises_error(tmp_path):
    """
    Test that an existing output file is not overwritten.
    """

    output_path = tmp_path / "result.xlsx"

    dataframe = pd.DataFrame({
        "Name": ["Alice"]
    })

    # Create the file first
    dataframe.to_excel(
        output_path,
        index=False
    )

    writer = ExcelWriter()

    with pytest.raises(FileExistsError):
        writer.write_to_excel(
            dataframe,
            output_path
        )