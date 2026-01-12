from pathlib import Path
from reconfig import resolve_config


def test_root_from_import_as_variable():
    root = Path("./test/test_configs/conf_from_import_one_as/root_root_from_import_as_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "imp_var": "imp_val",
    }

    assert result == expected


def test_child_from_import_as_variable():
    root = Path("./test/test_configs/conf_from_import_one_as/root_child_from_import_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "imp_var": "imp_val",
        },
    }

    assert result == expected


def test_root_from_import_as_section():
    root = Path("./test/test_configs/conf_from_import_one_as/root_root_from_import_as_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "imp_sec": {"section_var": "import_section_var_value"},
    }

    assert result == expected
    
def test_child_from_import_as_section():
    root = Path("./test/test_configs/conf_from_import_one_as/root_child_from_import_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "imp_sec": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected
    
def test_root_from_import_as_section_variable():
    root = Path("./test/test_configs/conf_from_import_one_as/root_root_from_import_section_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "sec_var": "import_section_var_value",
    }

    assert result == expected
    

def test_child_from_import_as_section_variable():
    root = Path("./test/test_configs/conf_from_import_one_as/root_child_from_import_section_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "sec_var": "import_section_var_value",
        },
    }

    assert result == expected


def test_root_from_import_as():
    root = Path("./test/test_configs/conf_from_import_one_as/root_root_from_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "imp_var": "imp_val",
    }

    assert result == expected


def test_child_from_import_as():
    root = Path("./test/test_configs/conf_from_import_one_as/root_child_from_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "imp_var": "imp_val",
        },
    }

    assert result == expected
