from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional, cast

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


def load_toml_dict(path: Path) -> dict:
    import tomllib

    with open(path, "rb") as f:
        toml_dict = tomllib.load(f)

    return toml_dict




def resolve_path(path:Path, base_path: Optional[Path] = None) -> Path:
    if base_path is None:
        return path.resolve()

    if path.is_absolute():
        return path.resolve()

    return (base_path.parent / path).resolve()

def resolve_inside_address(obj: dict[str, Any], inside_address: list[str]) -> Any:
    if not inside_address:
        return obj
    
    if not isinstance(obj, dict):
        raise ValueError(f"Cannot resolve inside address {inside_address} on non-dict object: {obj}")
    
    key, *rest = inside_address
    if key not in obj:
        raise KeyError(f"Key {key} not found in object while resolving inside address {inside_address}: {obj}")
    
    return resolve_inside_address(obj[key], rest)




@dataclass
class ConfigBuilder:
    base_path : Optional[Path] = None
    import_path_stack: List[Path] = field(default_factory=list)
    raw_toml_dict: dict[str, str] = field(default_factory=dict)
    delete_imports: bool = True

    loader: Callable[[Path], dict] = field(default_factory=lambda: load_toml_dict)

    @property
    def resolved_path(self) -> Path:
        return self.import_path_stack[-1].resolve()

    def imports(self) -> List[BaseImport]:
        reconfig = self.raw_toml_dict.get("imports", [])
        reconfig = cast(Iterable[dict], reconfig)
        return [detect_import(import_dict) for import_dict in reconfig]

    def child_environments(self) -> dict:
        return {
            name: d for name, d in self.raw_toml_dict.items() if isinstance(d, dict)
        }

    @property
    def reconfig_list(self) -> list[dict[str, dict]]:
        imps = self.raw_toml_dict.get("imports", [])
        imps = cast(list[dict[str, dict]], imps)
        return imps

    def resolve_recursive_imports(self) -> dict[str, Any]:
        result_config: dict[str, Any] = self.raw_toml_dict.copy()
        if "imports" in result_config:
            del result_config["imports"]

        # resolve the imports at the top level
        for imp in self.imports():
            import_path = resolve_path(self.resolved_path, base_path=self.base_path)
            if import_path in self.import_path_stack:
                raise ValueError(
                    f"Circular import detected: {import_path} is already in the import stack: {self.import_path_stack}"
                )

            import_dict = self.loader(import_path)

            builder = ConfigBuilder(
                base_path=import_path,
                import_path_stack=self.import_path_stack + [import_path],
                raw_toml_dict=import_dict,
                delete_imports=self.delete_imports,
            )
            resolved = builder.resolve_recursive_imports()
            inside_resolved = resolve_inside_address(obj=resolved, inside_address=imp.inside_address)

            match imp:
                case Import( _ ) :              
                    import_to_name = imp.filepath.stem
                    if import_to_name in result_config:
                        raise ValueError(
                            f"Import conflict: {import_to_name} already exists in the configuration. {imp}"
                        )
                        
                    result_config[import_to_name] = inside_resolved

                case ImportAs( _, as_name=as_name, ):
                    if as_name in result_config:
                        raise ValueError(
                            f"Import conflict: {as_name} already exists in the configuration. {imp}"
                        )
                    
                    result_config[as_name] = inside_resolved

                case FromImportOne(_, import_name=import_name):

                    if import_name in result_config:
                        raise ValueError(
                            f"Import conflict: {import_name} already exists in the configuration. {result_config} {imp}"
                        )
                        
                    result_config[import_name] = inside_resolved

                case FromImportMany(_, import_names=import_names):                    
                    
                    for import_name in import_names:
                        
                        if import_name in result_config:
                            raise ValueError(
                                f"Import conflict: {import_name} already exists in the configuration. {imp}"
                            )
                        if import_name not in inside_resolved:
                            raise ValueError(
                                f"Import name {import_name} not found in {imp}."
                            )
                            
                        result_config[import_name] = inside_resolved[import_name]

                case FromImportStar(_):
                    for import_name, value in inside_resolved.items():
                        if import_name in result_config:
                            raise ValueError(
                                f"Import conflict: {import_name} already exists in the configuration. {imp}"
                            )
                        result_config[import_name] = value

                case FromImportOneAs(
                    _, import_name=import_name, as_name=as_name
                ):
                    if as_name in result_config:
                        raise ValueError(
                            f"Import conflict: {as_name} already exists in the configuration. {imp}"
                        )
                    if import_name not in inside_resolved:
                        raise ValueError(
                            f"Import name {import_name} not found in {imp.filepath}. {imp}"
                        )
                                           
                    result_config[as_name] = inside_resolved[import_name]

                case _:
                    raise NotImplementedError(
                        f"Import type {type(imp)} not implemented yet. {imp}"
                    )

        # resolve the child environments
        for name, d in self.child_environments().items():
            b = ConfigBuilder(
                base_path=self.base_path,
                import_path_stack=self.import_path_stack,
                raw_toml_dict=d,
                delete_imports=self.delete_imports,
            )
            resolved_d = b.resolve_recursive_imports()
            result_config[name] = resolved_d

        return result_config
