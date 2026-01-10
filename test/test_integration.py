from reconfig import resolve_config


def test_readme_example(tmp_path):
    """Test the example configuration from README.md"""
    
    # Create directory structure
    includes_a = tmp_path / "includes_A"
    includes_b = tmp_path / "includes_B"
    etc_dir = tmp_path / "etc" / "reconf"
    
    includes_a.mkdir(parents=True)
    includes_b.mkdir(parents=True)
    etc_dir.mkdir(parents=True)
    
    # Create /etc/reconf/etc_conf.toml
    etc_conf = etc_dir / "etc_conf.toml"
    etc_conf.write_text('''etc_var = "etc"
''')
    
    # Create ./includes_B/include_d.toml
    include_d = includes_b / "include_d.toml"
    include_d.write_text('''var_d = "value_d_yes"

[section_d]
section_d_var_d = "section_d_value_d"

[section_e]
var_section_e = "not present"
''')
    
    # Create ./includes_A/include_a.toml
    include_a = includes_a / "include_a.toml"
    etc_path = etc_conf.resolve().as_posix()
    assert etc_path.endswith("etc/reconf/etc_conf.toml")
    assert etc_path.startswith("/")
    include_a.write_text(f'''imports = [
    {{import = "../includes_B/include_d.toml"}},
    {{import = "{etc_path}"}}
]

var_a = "value_a"
''')
    
    # Create ./includes_A/include_b.toml
    include_b = includes_a / "include_b.toml"
    include_b.write_text('''var_b = "value_b"

[section_in_b]
var_in_section_b = "value_in_section_b"
''')
    
    # Create ./includes_A/include_c.toml
    include_c = includes_a / "include_c.toml"
    include_c.write_text('''var_c = "value_c"
var_d = "value_d"
''')
    
    # Create ./root.toml
    root_toml = tmp_path / "root.toml"
    root_toml.write_text('''imports = [
    {import = "./includes_A/include_a.toml"},
]

[section]
imports = [
    {from = "./includes_A/include_b.toml", import = "var_b"},
    {from = "./includes_A/include_c.toml", import = "var_c", as="new_var_c"},
    {from = "./includes_B/include_d.toml", import = ["var_d", "section_d"]}
]
''')
    
    # Resolve configuration
    result = resolve_config(root_toml)
    
    # Assert expected structure from README
    expected = {
        "include_a": {
            "include_d": {
                "var_d": "value_d_yes",
                "section_d": {
                    "section_d_var_d": "section_d_value_d"
                },
                "section_e": {
                    "var_section_e": "not present"
                }
            },
            "etc_conf": {
                "etc_var": "etc"
            },
            "var_a": "value_a"
        },
        "section": {
            "var_b": "value_b",
            "new_var_c": "value_c",
            "var_d": "value_d_yes",
            "section_d": {
                "section_d_var_d": "section_d_value_d"
            }
        }
    }
    
    assert result == expected
