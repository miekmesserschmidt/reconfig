
def test_double_dot_import():
    """Test that double dot imports work correctly."""
    from pathlib import Path
    from reconfig import resolve_config

    root = Path("./test/test_configs/conf_double_dot_import/root.toml")
    result = resolve_config(root)

    expected = {
        "var": "val",
    }

    assert result == expected