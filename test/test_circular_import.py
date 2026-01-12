from pathlib import Path
from reconfig import resolve_config
import pytest


def test_circular_import_detection():
    """Test that circular imports are detected and raise an appropriate error."""
    root = Path("./test/error_configs/conf_circular_import/root.toml")
    
    # The circular import chain is: root -> a -> b -> a
    # This should raise an error (either RecursionError or a custom circular import error)
    with pytest.raises( ValueError ):
        resolve_config(root)
