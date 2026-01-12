from pathlib import Path
from reconfig import resolve_config


def test_root_from_import_section_variables():
    root = Path("./test/test_configs/conf_from_import_many/root_root_from_import_section_variables.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "section_var0": "sec_val0",
        "section_var1": "sec_val1",
        "child_section": {
            "ch_var": "child_value",
        },
    }

    assert result == expected


def test_child_from_import_section_variables():
    root = Path("./test/test_configs/conf_from_import_many/root_child_from_import_section_variables.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "section_var0": "sec_val0",
            "section_var1": "sec_val1",
        },
    }

    assert result == expected


def test_root_from_import_section_sections():
    root = Path("./test/test_configs/conf_from_import_many/root_root_from_import_section_sections.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_section0": {
            "section_var0": "sec_val0",
            "section_var1": "sec_val1",
            "section_var2": "sec_val2",
        },
        "import_section1": {
            "section_var0": "sec_val0",
            "section_var1": "sec_val1",
            "section_var2": "sec_val2",
        },
        "child_section": {
            "ch_var": "child_value",
        },
    }

    assert result == expected


def test_child_from_import_section_sections():
    root = Path("./test/test_configs/conf_from_import_many/root_child_from_import_section_sections.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_section0": {
                "section_var0": "sec_val0",
                "section_var1": "sec_val1",
                "section_var2": "sec_val2",
            },
            "import_section1": {
                "section_var0": "sec_val0",
                "section_var1": "sec_val1",
                "section_var2": "sec_val2",
            },
        },
    }

    assert result == expected


def test_root_from_import_hybrid():
    root = Path("./test/test_configs/conf_from_import_many/root_root_from_import_hybrid.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "import_section0": {
            "section_var0": "sec_val0",
            "section_var1": "sec_val1",
            "section_var2": "sec_val2",
        },
        "import_var2": "imp_val2",
        "child_section": {
            "ch_var": "child_value",
        },
    }

    assert result == expected


def test_child_from_import_hybrid():
    root = Path("./test/test_configs/conf_from_import_many/root_child_from_import_hybrid.toml")
    result = resolve_config(root)

    expected = {
        "var_root": "root_value",
        "child_section": {
            "import_section0": {
                "section_var0": "sec_val0",
                "section_var1": "sec_val1",
                "section_var2": "sec_val2",
            },
            "import_var2": "imp_val2",
        },
    }

    assert result == expected
