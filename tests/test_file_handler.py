from pathlib import Path

import pytest

from src.modules.file_handler import FileHandler


def test_validate_file_exists(tmp_path):
    """
    Test that validate_file_exists returns True
    when the file exists.
    """

    # Create a temporary test file
    test_file = tmp_path / "test.xlsx"
    test_file.touch()

    # Initialize FileHandler
    file_handler = FileHandler()

    # Validate file
    result = file_handler.validate_file_exists(test_file)

    # Verify result
    assert result is True


def test_validate_file_does_not_exist(tmp_path):
    """
    Test that validate_file_exists raises FileNotFoundError
    when the file does not exist.
    """

    # Define a file that does not exist
    test_file = tmp_path / "missing.xlsx"

    # Initialize FileHandler
    file_handler = FileHandler()

    # Verify that FileNotFoundError is raised
    with pytest.raises(FileNotFoundError):
        file_handler.validate_file_exists(test_file)