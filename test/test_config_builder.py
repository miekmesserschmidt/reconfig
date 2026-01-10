import pytest
from pathlib import Path
from reconfig.reconfig import ConfigBuilder


class TestConfigBuilderHappy:
    """Test happy path scenarios with valid configurations."""
    
    def test_basic_import(self):
        """Test basic import without alias."""
        config_path = Path("test/configs/happy/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        result = builder.resolve_recursive_imports()
        
        # Check that includes were imported with their file stem as key
        assert "include1" in result
        assert "include2" not in result  # renamed to custom_name_include2
        assert "custom_name_include2" in result
        assert "section_b" in result
        
        # Check values from include1
        assert result["include1"]["val0"] == "val0"
        assert result["include1"]["val1"] == "val1"
        
        # Check values from include2 (renamed)
        assert result["custom_name_include2"]["val3"] == "value3"
        assert result["custom_name_include2"]["val4"] == "value4"
        
        # Check section_b from include3
        assert result["section_b"]["val_b1"] == "value_b1"
        assert result["section_b"]["val_b2"] == "value_b2"
        
    def test_nested_section_imports(self):
        """Test imports within nested sections."""
        config_path = Path("test/configs/happy/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        result = builder.resolve_recursive_imports()
        
        # Check section_a has all its imports
        assert "section_a" in result
        section_a = result["section_a"]
        
        assert "include1" in section_a
        assert "custom_name_include2" in section_a
        assert "section_a" in section_a  # from include3
        assert "section_b" in section_a  # from include3
        assert "renamed_section_a" in section_a
        
        # Verify values in nested imports
        assert section_a["section_a"]["val_a1"] == "value_a1"
        assert section_a["renamed_section_a"]["val_a1"] == "value_a1"


class TestConfigBuilderCircularImport:
    """Test circular import detection."""
    
    def test_circular_import_detected(self):
        """Test that circular imports raise ValueError."""
        config_path = Path("test/configs/circular_import/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Circular import detected"):
            builder.resolve_recursive_imports()


class TestConfigBuilderImportConflicts:
    """Test various import conflict scenarios."""
    
    def test_import_conflict(self):
        """Test that importing the same file twice raises ValueError."""
        config_path = Path("test/configs/import_conflict/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_import_as_conflict(self):
        """Test that importing with duplicate alias names raises ValueError."""
        config_path = Path("test/configs/import_as_conflict/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_one_conflict(self):
        """Test that importing the same section twice raises ValueError."""
        config_path = Path("test/configs/from_import_one_conflict/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_many_conflict(self):
        """Test that importing overlapping sections raises ValueError."""
        config_path = Path("test/configs/from_import_many_conflict/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_as_conflict(self):
        """Test that importing sections with duplicate alias names raises ValueError."""
        config_path = Path("test/configs/from_import_as_conflict/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()


class TestConfigBuilderMethods:
    """Test individual ConfigBuilder methods."""
    
    def test_load_toml_dict(self):
        """Test loading TOML file into dictionary."""
        config_path = Path("test/configs/happy/root.toml")
        result = ConfigBuilder.load_toml_dict(config_path)
        
        assert isinstance(result, dict)
        assert "reconfig" in result
        assert isinstance(result["reconfig"], list)
    
    def test_imports_method(self):
        """Test extracting imports from raw TOML dict."""
        config_path = Path("test/configs/happy/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        imports = builder.imports()
        assert isinstance(imports, list)
        assert len(imports) == 3
    
    def test_child_environments(self):
        """Test extracting child environment sections."""
        config_path = Path("test/configs/happy/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        children = builder.child_environments()
        assert isinstance(children, dict)
        assert "section_a" in children
        assert isinstance(children["section_a"], dict)
    
    def test_reconfig_list_property(self):
        """Test reconfig_list property returns the reconfig array."""
        config_path = Path("test/configs/happy/root.toml").resolve()
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        reconfig_list = builder.reconfig_list
        assert isinstance(reconfig_list, list)
        assert len(reconfig_list) > 0
    
    def test_reconfig_removed_from_result(self):
        """Test that reconfig key is removed from resolved config."""
        config_path = Path("test/configs/happy/root.toml")
        toml_dict = ConfigBuilder.load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        result = builder.resolve_recursive_imports()
        assert "reconfig" not in result
