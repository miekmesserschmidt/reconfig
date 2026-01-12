from pathlib import Path
from reconfig import resolve_config


def test_root_from_import():
    root = Path("./test/test_configs/conf_from_import_one/root_root_from_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_var": "imp_val",
    }

    assert result == expected


def test_child_from_import():
    root = Path("./test/test_configs/conf_from_import_one/root_child_from_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_var": "imp_val",
        },
    }

    assert result == expected


def test_root_from_import_variable():
    root = Path("./test/test_configs/conf_from_import_one/root_root_from_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_var": "imp_val",
    }

    assert result == expected


def test_child_from_import_variable():
    root = Path("./test/test_configs/conf_from_import_one/root_child_from_import_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_var": "imp_val",
        },
    }

    assert result == expected


def test_root_from_import_section():
    root = Path("./test/test_configs/conf_from_import_one/root_root_from_import_as_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_section": {"section_var": "import_section_var_value"},
    }

    assert result == expected
    
def test_child_from_import_section():
    root = Path("./test/test_configs/conf_from_import_one/root_child_from_import_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_section": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected
    
def test_root_from_import_section_variable():
    root = Path("./test/test_configs/conf_from_import_one/root_root_from_import_section_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "section_var": "import_section_var_value",
    }

    assert result == expected
    

def test_child_from_import_section_variable():
    root = Path("./test/test_configs/conf_from_import_one/root_child_from_import_section_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "section_var": "import_section_var_value",
        },
    }

    assert result == expected


def test_root_from_import_as_variable():
    root = Path("./test/test_configs/conf_from_import_one/root_root_from_import_as_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_var": "imp_val",
    }

    assert result == expected
