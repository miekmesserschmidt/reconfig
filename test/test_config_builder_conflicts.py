import pytest
from pathlib import Path
from reconfig.reconfig import ConfigBuilder, load_toml_dict


class TestConfigBuilderCircularImport:
    """Test circular import detection."""
    
    def test_circular_import_detected(self):
        """Test that circular imports raise ValueError."""
        config_path = Path("test/configs/circular_import/root.toml")
        toml_dict = load_toml_dict(config_path)
        
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
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_import_as_conflict(self):
        """Test that importing with duplicate alias names raises ValueError."""
        config_path = Path("test/configs/import_as_conflict/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_one_conflict(self):
        """Test that importing the same section twice raises ValueError."""
        config_path = Path("test/configs/from_import_one_conflict/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_many_conflict(self):
        """Test that importing overlapping sections raises ValueError."""
        config_path = Path("test/configs/from_import_many_conflict/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()
    
    def test_from_import_as_conflict(self):
        """Test that importing sections with duplicate alias names raises ValueError."""
        config_path = Path("test/configs/from_import_as_conflict/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import conflict.*already exists"):
            builder.resolve_recursive_imports()


class TestConfigBuilderImportNameMissing:
    """Test scenarios where imported section names don't exist in the target file."""
    
    def test_from_import_one_name_missing(self):
        """Test that importing a non-existent section raises ValueError."""
        config_path = Path("test/configs/from_import_one_name_missing/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import name.*not found"):
            builder.resolve_recursive_imports()
    
    def test_from_import_many_name_missing(self):
        """Test that importing with one or more non-existent sections raises ValueError."""
        config_path = Path("test/configs/from_import_many_name_missing/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import name.*not found"):
            builder.resolve_recursive_imports()
    
    def test_from_import_as_name_missing(self):
        """Test that importing a non-existent section with alias raises ValueError."""
        config_path = Path("test/configs/from_import_as_name_missing/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Import name.*not found"):
            builder.resolve_recursive_imports()


class TestConfigBuilderInvalidImport:
    """Test scenarios with invalid import syntax."""
    
    def test_invalid_import_definition(self):
        """Test that invalid import definitions raise ValueError."""
        config_path = Path("test/configs/imports_invalid_import/root.toml")
        toml_dict = load_toml_dict(config_path)
        
        builder = ConfigBuilder(
            import_path_stack=[config_path],
            raw_toml_dict=toml_dict,
        )
        
        with pytest.raises(ValueError, match="Invalid import definition"):
            builder.resolve_recursive_imports()
