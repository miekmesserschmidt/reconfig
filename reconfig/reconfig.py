from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, List, cast

from reconfig.import_types import (
    FromImportMany,
    detect_import,
    BaseImport,
    Import,
    ImportAs,
    FromImportOne,
    FromImportAs,
)


def load_toml_dict(path: Path) -> dict:
    import tomllib

    with open(path, "rb") as f:
        toml_dict = tomllib.load(f)

    return toml_dict


@dataclass
class ConfigBuilder:
    import_path_stack: List[Path]
    raw_toml_dict: dict[str,str]
    delete_imports: bool = True
    
    loader : Callable[[Path], dict] = field(default_factory=lambda: load_toml_dict)

    
    
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
        result_config : dict[str, Any] = self.raw_toml_dict.copy()
        if "imports" in result_config:
            del result_config["imports"]

        # resolve the imports at the top level
        for imp in self.imports():
            import_path = imp.resolve_path(self.resolved_path)
            if import_path in self.import_path_stack:
                raise ValueError(
                    f"Circular import detected: {import_path} is already in the import stack: {self.import_path_stack}"
                )

            import_dict = self.loader(import_path)

            builder = ConfigBuilder(
                import_path_stack=self.import_path_stack + [import_path],
                raw_toml_dict=import_dict,
                delete_imports=self.delete_imports,
            )
            resolved = builder.resolve_recursive_imports()

            match imp:
                case Import(path=path):
                    fn = path.stem
                    if fn in result_config:
                        raise ValueError(
                            f"Import conflict: {fn} already exists in the configuration."
                        )
                    result_config[fn] = resolved

                case ImportAs(path=path, as_name=as_name):
                    if as_name in result_config:
                        raise ValueError(
                            f"Import conflict: {as_name} already exists in the configuration."
                        )
                    result_config[as_name] = resolved

                case FromImportOne(path=path, import_name=import_name):
                    if import_name in result_config:
                        raise ValueError(
                            f"Import conflict: {import_name} already exists in the configuration."
                        )
                    if import_name not in resolved:
                        raise ValueError(
                            f"Import name {import_name} not found in {path}."
                        )
                    result_config[import_name] = resolved[import_name]

                case FromImportMany(path=path, import_names=import_names):
                    for import_name in import_names:
                        if import_name not in resolved:
                            raise ValueError(
                                f"Import name {import_name} not found in {path}."
                            )
                        if import_name in result_config:
                            raise ValueError(
                                f"Import conflict: {import_name} already exists in the configuration."
                            )
                        result_config[import_name] = resolved[import_name]

                case FromImportAs(path=path, import_name=import_name, as_name=as_name):
                    if import_name not in resolved:
                        raise ValueError(
                            f"Import name {import_name} not found in {path}."
                        )
                    if as_name in result_config:
                        raise ValueError(
                            f"Import conflict: {as_name} already exists in the configuration."
                        )
                    result_config[as_name] = resolved[import_name]

                case _:
                    raise NotImplementedError(
                        f"Import type {type(imp)} not implemented yet."
                    )

        # resolve the child environments
        for name, d in self.child_environments().items():
            b = ConfigBuilder(
                import_path_stack=self.import_path_stack,
                raw_toml_dict=d,
                delete_imports=self.delete_imports,
            )
            resolved_d = b.resolve_recursive_imports()
            result_config[name] = resolved_d
            
        return result_config