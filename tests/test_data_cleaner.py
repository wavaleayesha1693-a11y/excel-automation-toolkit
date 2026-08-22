import pandas as pd

from src.modules.data_cleaner import DataCleaner


def test_remove_duplicate_rows():
    """
    Test that duplicate rows are removed.
    """

    dataframe = pd.DataFrame({
        "Name": ["Alice", "Alice", "Bob"],
        "Salary": [50000, 50000, 60000]
    })

    cleaner = DataCleaner()

    result = cleaner.remove_duplicate_rows(dataframe)

    assert len(result) == 2
    assert result["Name"].tolist() == ["Alice", "Bob"]


def test_get_missing_value_report():
    """
    Test that missing-value report is generated correctly.
    """

    dataframe = pd.DataFrame({
        "Name": ["Alice", None, "Bob"],
        "Salary": [50000, 60000, None]
    })

    cleaner = DataCleaner()

    result = cleaner.get_missing_value_report(dataframe)

    assert list(result.columns) == [
        "Column",
        "Missing Count",
        "Missing_Percentage"
    ]

    name_missing = result.loc[
        result["Column"] == "Name",
        "Missing Count"
    ].iloc[0]

    salary_missing = result.loc[
        result["Column"] == "Salary",
        "Missing Count"
    ].iloc[0]

    assert name_missing == 1
    assert salary_missing == 1


def test_fill_missing_values():
    """
    Test that missing numeric values become 0
    and missing string values become 'Unknown'.
    """

    dataframe = pd.DataFrame({
        "Name": ["Alice", None],
        "Salary": [50000, None]
    })

    cleaner = DataCleaner()

    result = cleaner.fill_missing_values(dataframe)

    assert result["Name"].iloc[1] == "Unknown"
    assert result["Salary"].iloc[1] == 0

    assert result.isna().sum().sum() == 0