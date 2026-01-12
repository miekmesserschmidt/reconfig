from pathlib import Path
from reconfig import resolve_config


def test_integration():
    """Integration test based on the README.md example."""
    root = Path("./test/test_configs/conf_integration/root.toml")
    result = resolve_config(root)

    expected = {
        "recursive": {
            "a": {"var_a": "val_a"},
            "b": {"var_b": "val_b", "section_b": {"sec_val_b": "sec_val_b"}},
            "c": {
                "var_c": "val_c",
                "section_c": {
                    "section_var_c0": "sec_val_c0",
                    "section_var_c1": "sec_val_c1",
                    "section_var_c2": "sec_val_c2",
                },
            },
        },
        "section": {
            "var_a": "val_a",
            "a_renamed": {"var_a": "val_a"},
            "var_b": "val_b",
            "sec_val_b": "sec_val_b",
            "renamed_sec_val_b": "sec_val_b",
            "var_c": "val_c",
            "section_c": {
                "section_var_c0": "sec_val_c0",
                "section_var_c1": "sec_val_c1",
                "section_var_c2": "sec_val_c2",
            },
            "section_var_c0": "sec_val_c0",
            "section_var_c2": "sec_val_c2",
        },
    }

    assert result == expected
