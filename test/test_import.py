from pathlib import Path
from reconfig import resolve_config


def test_root_import():
    root = Path("./test/test_configs/conf_import/root_root_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "incl": {
            "import_var": "imp_val",
            "import_section": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected


def test_child_import():
    root = Path("./test/test_configs/conf_import/root_child_import.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "incl": {
                "import_var": "imp_val",
                "import_section": {"section_var": "import_section_var_value"},
            },
        },
    }

    assert result == expected


def test_root_import_variable():
    root = Path("./test/test_configs/conf_import/root_root_import_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_var": "imp_val",
    }

    assert result == expected


def test_child_import_variable():
    root = Path("./test/test_configs/conf_import/root_child_import_variable.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_var": "imp_val",
        },
    }

    assert result == expected


def test_root_import_section():
    root = Path("./test/test_configs/conf_import/root_root_import_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_section": {"section_var": "import_section_var_value"},
    }

    assert result == expected


def test_child_import_section():
    root = Path("./test/test_configs/conf_import/root_child_import_section.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_section": {"section_var": "import_section_var_value"},
        },
    }

    assert result == expected


def test_root_import_section_variable():
    root = Path(
        "./test/test_configs/conf_import/root_root_import_section_variable.toml"
    )
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "section_var": "import_section_var_value",
    }

    assert result == expected


def test_child_import_section_variable():
    root = Path(
        "./test/test_configs/conf_import/root_child_import_section_variable.toml"
    )
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "section_var": "import_section_var_value",
        },
    }

    assert result == expected
