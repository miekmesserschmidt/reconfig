from pathlib import Path
from reconfig import resolve_config
import pytest


def test_override_import_name():
    """Test that an import with 'as' correctly overrides existing keys."""
    root = Path("./test/error_configs/conf_override_import_name/root_a.toml")
    
    with pytest.raises( ValueError):
        resolve_config(root)
    
def test_override():
    """Test that an import with 'as' correctly overrides existing keys."""
    root = Path("./test/error_configs/conf_override/root_a.toml")
    
    with pytest.raises( ValueError):
        resolve_config(root)

def test_override_import_star():
    """Test that an import with '*' correctly overrides existing keys."""
    root = Path("./test/error_configs/conf_override_import_star/root_a.toml")
    
    with pytest.raises( ValueError):
        resolve_config(root)