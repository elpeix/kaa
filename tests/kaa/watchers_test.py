from kaa.watchers import ElementValidator


def test_validate_no_restrictions():
    validator = ElementValidator([], [])
    assert validator.is_valid("file")
    assert validator.is_valid(".hidden")


def test_validate_blank_element():
    validator = ElementValidator([], [])
    assert not validator.is_valid("")
    assert not validator.is_valid("  ")


def test_validate_inclusions():
    validator = ElementValidator(["file", "other_file", ".hidden", "*.py"], [])
    assert validator.is_valid("file")
    assert validator.is_valid("other_file")
    assert validator.is_valid(".hidden")
    assert not validator.is_valid("not_allowed")
    assert validator.is_valid("valid.py")


def test_validate_exclusions():
    validator = ElementValidator([], ["file", "other_file", ".hidden", "*.py"])
    assert not validator.is_valid("file")
    assert not validator.is_valid("other_file")
    assert not validator.is_valid(".hidden")
    assert validator.is_valid("not_allowed")
    assert not validator.is_valid("valid.py")


def test_validate():
    """Exclusions are priority"""
    validator = ElementValidator(
        ["src", "*.py", "*.log"],
        [".git", "__pycache__", "*.log"],
    )
    assert validator.is_valid("src")
    assert validator.is_valid("file.py")
    assert not validator.is_valid("file.log")
    assert not validator.is_valid(".git")
    assert not validator.is_valid("__pycache__")
