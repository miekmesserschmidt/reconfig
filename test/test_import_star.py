import pytest
from pathlib import Path
from reconfig.reconfig import ConfigBuilder, load_toml_dict


class TestFromImportStar:
    """Test 'from X import *' functionality."""

    def test_from_import_star_basic(self):
        """Test basic 'from X import *' imports all sections from target file."""
        config_path = Path("test/configs/from_import_star_happy/root.toml")
        toml_dict = load_toml_dict(config_path)

        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )

        result = builder.resolve_recursive_imports()

        # All sections from sections.toml should be imported
        assert "section_a" in result
        assert "section_b" in result
        assert "section_c" in result

        # Check values from imported sections
        assert result["section_a"]["value_a"] == "from_section_a"
        assert result["section_a"]["nested_a"] == "nested_value_a"
        assert result["section_b"]["value_b"] == "from_section_b"
        assert result["section_b"]["nested_b"] == "nested_value_b"
        assert result["section_c"]["value_c"] == "from_section_c"

        # Local section should also exist
        assert "local_section" in result
        assert result["local_section"]["local_value"] == "local_data"

    @pytest.mark.parametrize(
        "config_dir",
        [
            "from_import_star_conflict",
            "from_import_star_conflict_section",
        ],
    )
    def test_from_import_star_conflict(self, config_dir):
        """Test that 'from X import *' raises error when imported section conflicts with existing section."""
        config_path = Path(f"test/configs/{config_dir}/root.toml")
        toml_dict = load_toml_dict(config_path)

        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )

        # Should raise ValueError because value_a or section_a already exists
        with pytest.raises(
            ValueError,
            match="Import conflict.*value_a already exists.|Import conflict.*section_a already exists.",
        ):
            builder.resolve_recursive_imports()

    def test_from_import_star_empty_file(self):
        """Test that 'from X import *' works with empty file (imports nothing)."""
        config_path = Path("test/configs/from_import_star_empty/root.toml")
        toml_dict = load_toml_dict(config_path)

        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )

        result = builder.resolve_recursive_imports()

        # Should only have local section, nothing imported from empty file
        assert "local" in result
        assert result["local"]["value"] == "local_value"

        # No other sections should exist (imports key is removed)
        assert len(result) == 1

    def test_from_import_star_in_nested_sections(self):
        """Test that 'from X import *' works in nested sections."""
        config_path = Path("test/configs/from_import_star_nested/root.toml")
        toml_dict = load_toml_dict(config_path)

        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )

        result = builder.resolve_recursive_imports()

        # Check section_a has its subsection with star imports
        assert "section_a" in result
        assert "subsection" in result["section_a"]
        subsection = result["section_a"]["subsection"]

        # All sections from base.toml should be imported into subsection
        assert "db" in subsection
        assert "cache" in subsection
        assert subsection["db"]["host"] == "localhost"
        assert subsection["db"]["port"] == 5432
        assert subsection["cache"]["host"] == "redis.local"
        assert subsection["cache"]["ttl"] == 3600
        assert subsection["nested_local"] == "nested_data"

        # Check section_b also has star imports
        assert "section_b" in result
        section_b = result["section_b"]
        assert "db" in section_b
        assert "cache" in section_b
        assert section_b["db"]["host"] == "localhost"
        assert section_b["cache"]["ttl"] == 3600

    def test_from_import_star_isolated_scopes(self):
        """Test that 'from X import *' in different nested sections have isolated scopes."""
        config_path = Path("test/configs/from_import_star_nested/root.toml")
        toml_dict = load_toml_dict(config_path)

        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )

        result = builder.resolve_recursive_imports()

        # Both subsection and section_b import all from base.toml
        # They should have independent copies
        subsection = result["section_a"]["subsection"]
        section_b = result["section_b"]

        # Both should have db and cache
        assert "db" in subsection
        assert "db" in section_b
        assert "cache" in subsection
        assert "cache" in section_b

        # Values should match but be in separate scopes
        assert subsection["db"]["host"] == section_b["db"]["host"]
        assert subsection["cache"]["ttl"] == section_b["cache"]["ttl"]
