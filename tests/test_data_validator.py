import pandas as pd
import pytest

from src.modules.data_validator import DataValidator


def test_validate_required_columns_success():
    """
    Test validation when all required columns are present.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": [1, 2],
        "Name": ["Alice", "Bob"],
        "Salary": [50000, 60000]
    })

    validator = DataValidator()

    result = validator.validate_required_columns(
        dataframe,
        ["Employee_ID", "Name", "Salary"]
    )

    assert result is True


def test_validate_required_columns_missing():
    """
    Test validation when required columns are missing.
    """

    dataframe = pd.DataFrame({
        "Employee_ID": [1, 2],
        "Name": ["Alice", "Bob"]
    })

    validator = DataValidator()

    with pytest.raises(ValueError, match="Salary"):
        validator.validate_required_columns(
            dataframe,
            ["Employee_ID", "Name", "Salary"]
        )