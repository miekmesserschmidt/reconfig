from pathlib import Path
from typing import Any, Callable

from reconfig.import_types import (
    FromImportMany,
    detect_import,
    BaseImport,
    Import,
    ImportAs,
    FromImportOne,
    FromImportStar,
    FromImportOneAs,
)


type Loader = Callable[[Path], dict]


def load_toml_dict(path: Path) -> dict:
    import tomllib

    with open(path, "rb") as f:
        toml_dict = tomllib.load(f)

    return toml_dict


def resolve_path(base_path: Path, path_str_to_resolve: str) -> Path:
    path_to_resolve = Path(path_str_to_resolve)
    if path_to_resolve.is_absolute():
        return path_to_resolve.resolve()
    else:
        return (base_path.parent / path_to_resolve).resolve()


def resolve_inner_path(data: dict, inside_address: list[str]) -> Any:
    if inside_address == []:
        return data

    first, *rest = inside_address
    if first not in data:
        raise KeyError(
            f"Key '{first}' not found in data during inside address resolution."
        )
    return resolve_inner_path(data[first], rest)


def build_extender(imp: BaseImport, file_imported_data: dict) -> dict:
    resolved_inner = resolve_inner_path(file_imported_data, imp.inside_address)

    match imp:
        case Import():
            as_name = Path(imp.path_string).stem
            return {as_name: resolved_inner}
        case ImportAs(as_name=as_name):
            return {as_name: resolved_inner}
        case FromImportOne(import_name=import_name):
            return {import_name: resolved_inner[import_name]}
        case FromImportOneAs(import_name=import_name, as_name=as_name):
            return {as_name: resolved_inner[import_name]}
        case FromImportMany(import_names=import_names):
            return {name: resolved_inner[name] for name in import_names}
        case FromImportStar():
            return resolved_inner
    raise ValueError(f"Unsupported import type: {imp}")


def resolve(
    base_path: Path,
    initial_data: dict,
    import_path_stack: list[Path],
    loader: Loader,
) -> dict:
    # grab the child environments: dicts that are not imports
    ch_envs = {name: val for name, val in initial_data.items() if isinstance(val, dict)}

    # grab the list of imports
    ch_imports_list = initial_data.get("imports", [])

    output_data = initial_data.copy()
    
    # resolve the imports
    for ch_imp_dict in ch_imports_list:
        ch_imp = detect_import(ch_imp_dict)
        ch_abs_fn = resolve_path(base_path, ch_imp.path_string)
        ch_base_path = ch_abs_fn.parent
        ch_resolved_data = resolve(
            base_path=ch_base_path,
            initial_data=loader(ch_abs_fn),
            import_path_stack=import_path_stack + [ch_abs_fn],
            loader=loader,
        )
        ch_extender = build_extender(ch_imp, ch_resolved_data)

        if set(ch_extender) & set(output_data):
            raise ValueError(
                f"Import conflict: keys {set(ch_extender) & set(output_data)} already exist in the output data."
            )

        output_data.update(ch_extender)

    # resolve the child environments 
    for name, ch_data in ch_envs.items():
        output_data[name] = resolve(
            base_path=base_path,
            initial_data=ch_data,
            import_path_stack=import_path_stack,
            loader=loader,
        )

    return output_data
