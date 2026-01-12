from dataclasses import dataclass
from operator import add
from pathlib import Path
from typing import Any, Protocol


class BaseImport(Protocol):
    import_string: str
    
    @property
    def path_string(self) -> str:
        return self.import_string.split("::")[0]
        
    @property
    def inside_address(self) -> list[str]:
        parts = self.import_string.split("::")
        if len(parts) <= 1:
            return []
        return parts[1].split(".")
    



@dataclass
class Import(BaseImport):
    import_string: str


@dataclass
class ImportAs(BaseImport):
    import_string: str
    as_name: str


@dataclass
class FromImportOne(BaseImport):
    import_string: str
    import_name: str


@dataclass
class FromImportOneAs(BaseImport):
    import_string: str
    import_name: str
    as_name: str


@dataclass
class FromImportMany(BaseImport):
    import_string: str
    import_names: list[str]


@dataclass
class FromImportStar(BaseImport):
    import_string: str


def detect_import(import_dict: dict) -> BaseImport:
    match import_dict:

        case {"from" : from_str, "import" : import_name, "as" : as_name}:
            return FromImportOneAs(import_string=from_str, import_name=import_name, as_name=as_name)
        case {"from" : from_str, "import" : "*"}:
            return FromImportStar(import_string=from_str)
        case {"from" : from_str, "import" : [*import_names]}:
            return FromImportMany(import_string=from_str, import_names=import_names)
        case {"from" : from_str, "import" : import_name}:
            return FromImportOne(import_string=from_str, import_name=import_name)
        case {"import" : import_str, "as" : as_name}:
            return ImportAs(import_string=import_str, as_name=as_name)
        case {"import" : import_str}:
            return Import(import_string=import_str)        
        case _:
            raise ValueError(f"Invalid import definition: {import_dict}")
        