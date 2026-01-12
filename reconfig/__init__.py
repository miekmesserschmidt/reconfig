from pathlib import Path
from reconfig.reconfig import Loader, resolve


def load_toml_dict(path: Path) -> dict:
    import tomllib

    with open(path, "rb") as f:
        toml_dict = tomllib.load(f)

    return toml_dict


def resolve_config(root_path: Path, loader: Loader = load_toml_dict) -> dict:
    root_path = root_path.resolve()
    base_path = root_path.parent
    initial_data = loader(root_path)
    return resolve(
        base_path=base_path,
        initial_data=initial_data,
        import_path_stack=[root_path],
        loader=loader,
    )
