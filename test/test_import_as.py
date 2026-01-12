from pathlib import Path
from reconfig import resolve_config


def test_root_import_as():
    root = Path("./test/test_configs/conf_import_as/root_root_import_as.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "inc": {
            "import_var": "imp_val",
            "import_section": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected


def test_child_import_as():
    root = Path("./test/test_configs/conf_import_as/root_child_import_as.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "inc": {
                "import_var": "imp_val",
                "import_section": {"section_var": "import_section_var_value"},
            },
        },
    }

    assert result == expected


def test_root_import_as_variable():
    root = Path("./test/test_configs/conf_import_as/root_root_import_as_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "imp_var": "imp_val",
    }

    assert result == expected


def test_child_import_as_variable():
    root = Path("./test/test_configs/conf_import_as/root_child_import_as_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "imp_var": "imp_val",
        },
    }

    assert result == expected


def test_root_import_as_section():
    root = Path("./test/test_configs/conf_import_as/root_root_import_as_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "sec": {"section_var": "import_section_var_value"},
    }

    assert result == expected
    
def test_child_import_as_section():
    root = Path("./test/test_configs/conf_import_as/root_child_import_as_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "sec": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected
    
def test_root_import_as_section_variable():
    root = Path("./test/test_configs/conf_import_as/root_root_import_as_section_as_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "sec_var": "import_section_var_value",
    }

    assert result == expected
    

def test_child_import_as_section_variable():
    root = Path("./test/test_configs/conf_import_as/root_child_import_as_section_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "sec_var": "import_section_var_value",
        },
    }

    assert result == expected

def test_miss_override_import_as():
    root = Path("test/test_configs/conf_override_import_as/root_a.toml")
    
    result = resolve_config(root)
    expected = {
        "a": "a_value",
        "b": "override_a",
    }
    
    assert result == expected