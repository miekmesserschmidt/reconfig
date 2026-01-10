
from pathlib import Path
from typing import Callable
from reconfig.reconfig import ConfigBuilder, load_toml_dict

def resolve_config(import_path: Path, loader: Callable[[Path], dict] = load_toml_dict ) -> dict:
    """_summary_

    Args:
        import_path (Path): Path of the initial config file to load.
        loader (Callable[[Path], dict], optional): The file loader used to load paths into dicts. Defaults to load_toml_dict.

    Returns:
        dict: the resolved configuration dictionary.
    """
    
    
    raw_data = loader(import_path)
    builder = ConfigBuilder(
        import_path_stack=[import_path],
        raw_toml_dict=raw_data,
        loader=loader,
    )
    return builder.resolve_recursive_imports()

