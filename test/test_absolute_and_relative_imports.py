from reconfig import resolve_config

ROOT = """
imports = [
    {import = "abs_fn"},
    {import = "rel.toml"},
    {import = "./dot_rel.toml"},    
]
"""

REL = """
rel_var = "relative_import_value"
"""

DOT_REL = """
dot_rel_var = "dot_relative_import_value"
"""

ABS = """
abs_var = "absolute_import_value"
"""


def test_absolute_and_relative_imports(tmp_path):
    """Test that both absolute and relative import paths work correctly."""

    # Create a temporary configuration structure
    root_config = tmp_path / "root.toml"
    abs_config = tmp_path / "abs.toml"
    rel_config = tmp_path / "rel.toml"
    dot_rel_config = tmp_path / "dot_rel.toml"

    abs_fn = abs_config.resolve()
    abs_fn_str = str(abs_fn)
    assert abs_fn_str.startswith("/")

    ROOT_CONTENT = ROOT.replace("abs_fn", abs_fn_str)
    root_config.write_text(ROOT_CONTENT)
    abs_config.write_text(ABS)
    rel_config.write_text(REL)
    dot_rel_config.write_text(DOT_REL)

    # Resolve the root configuration
    result = resolve_config(root_config)
    expected = {
        "abs": {"abs_var": "absolute_import_value"},
        "rel": {"rel_var": "relative_import_value"},
        "dot_rel": {"dot_rel_var": "dot_relative_import_value"},
    }
    assert result == expected
