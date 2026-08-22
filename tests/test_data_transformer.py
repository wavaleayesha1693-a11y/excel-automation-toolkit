import pandas as pd
import pytest

from src.modules.data_transformer import DataTransformer


def test_strip_whitespace():
    """
    Test that leading and trailing whitespace is removed.
    """

    dataframe = pd.DataFrame({
        "Name": [" Alice ", " Bob "],
        "Department": [" IT ", " HR "]
    })

    transformer = DataTransformer()

    result = transformer.strip_whitespace(dataframe)

    assert result["Name"].tolist() == ["Alice", "Bob"]
    assert result["Department"].tolist() == ["IT", "HR"]


def test_standardize_text_lower():
    """
    Test conversion of string columns to lowercase.
    """

    dataframe = pd.DataFrame({
        "Name": ["Alice", "BOB"],
        "Department": ["IT", "Human Resources"]
    })

    transformer = DataTransformer()

    result = transformer.standardize_text(
        dataframe,
        case="lower"
    )

    assert result["Name"].tolist() == ["alice", "bob"]
    assert result["Department"].tolist() == [
        "it",
        "human resources"
    ]


def test_standardize_text_invalid_case():
    """
    Test that an invalid case option raises ValueError.
    """

    dataframe = pd.DataFrame({
        "Name": ["Alice", "Bob"]
    })

    transformer = DataTransformer()

    with pytest.raises(ValueError):
        transformer.standardize_text(
            dataframe,
            case="invalid"
        )


def test_rename_columns():
    """
    Test that existing columns are renamed correctly.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": [1, 2],
        "Name": ["Alice", "Bob"]
    })

    transformer = DataTransformer()

    result = transformer.rename_columns(
        dataframe,
        {
            "Employee_ID": "Emp_ID",
            "Name": "Employee_Name"
        }
    )

    assert "Emp_ID" in result.columns
    assert "Employee_Name" in result.columns
    assert "Employee_ID" not in result.columns
    assert "Name" not in result.columns


def test_rename_columns_missing_column():
    """
    Test that missing columns are skipped
    while existing columns are still renamed.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": [1, 2],
        "Name": ["Alice", "Bob"]
    })

    transformer = DataTransformer()

    result = transformer.rename_columns(
        dataframe,
        {
            "Employee_ID": "Emp_ID",
            "Department": "Dept_Name"
        }
    )

    assert "Emp_ID" in result.columns
    assert "Department" not in result.columns
    assert "Dept_Name" not in result.columns


def test_convert_data_types():
    """
    Test successful conversion of multiple data types.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": ["1", "2"],
        "Salary": ["50000.50", "60000.75"],
        "Name": [100, 200]
    })

    transformer = DataTransformer()

    result = transformer.convert_data_types(
        dataframe,
        {
            "Employee_ID": "int",
            "Salary": "float",
            "Name": "string"
        }
    )

    assert str(result["Employee_ID"].dtype) == "Int64"
    assert result["Salary"].dtype == float
    assert str(result["Name"].dtype) == "string"


def test_convert_data_types_unsupported_type():
    """
    Test that unsupported data types generate a warning
    and do not stop other conversions.
    """

    dataframe = pd.DataFrame({
        "Salary": ["50000", "60000"],
        "Name": ["Alice", "Bob"]
    })

    transformer = DataTransformer()

    result = transformer.convert_data_types(
        dataframe,
        {
            "Salary": "currency",
            "Name": "string"
        }
    )

    assert result["Name"].dtype.name == "string"
    assert result["Salary"].tolist() == ["50000", "60000"]


def test_transform_pipeline():
    """
    Test the complete transformation pipeline.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": ["1", "2"],
        "Name": [" Alice ", " Bob "],
        "Salary": ["50000", "60000"]
    })

    transformer = DataTransformer()

    result = transformer.transform(
        dataframe,
        case="lower",
        column_mapping={
            "Employee_ID": "Emp_ID",
            "Name": "Employee_Name",
            "Salary": "Annual_Salary"
        },
        dtype_mapping={
            "Emp_ID": "int",
            "Annual_Salary": "float"
        }
    )

    assert list(result.columns) == [
        "Emp_ID",
        "Employee_Name",
        "Annual_Salary"
    ]

    assert result["Employee_Name"].tolist() == [
        "alice",
        "bob"
    ]

    assert str(result["Emp_ID"].dtype) == "Int64"
    assert result["Annual_Salary"].dtype == float