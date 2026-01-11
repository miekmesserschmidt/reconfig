from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional, Protocol




class BaseImport(Protocol):
    address_string: str

    @property
    def filepath(self) -> Path:
        if "::" in self.address_string:
            file_path, *_ = self.address_string.split("::")
            return Path(file_path)
        else:
            return Path(self.address_string)

    @property
    def inside_address(self) -> list[str]:
        if "::" in self.address_string:
            _, inside_path = self.address_string.split("::", 1)
            inside_addr = inside_path.split(".")
            return inside_addr
        else:
            return []

@dataclass
class Import(BaseImport):
    address_string: str


@dataclass
class ImportAs(BaseImport):
    address_string: str
    as_name: str


@dataclass
class FromImportOne(BaseImport):
    address_string: str
    import_name: str


@dataclass
class FromImportOneAs(BaseImport):
    address_string: str
    import_name: str
    as_name: str


@dataclass
class FromImportMany(BaseImport):
    address_string: str
    import_names: list[str]


@dataclass
class FromImportStar(BaseImport):
    address_string: str


def detect_import(import_dict: dict) -> BaseImport:
    match import_dict:
        case {"from": address_str, "import": "*"}:
            return FromImportStar(address_string=address_str)

        case {"from": address_str, "import": [*import_names] }:
            return FromImportMany(
                address_string=address_str,
                import_names=import_names,
            )

        case {"from": address_str, "import": import_name}:
            return FromImportOne(
                address_string=address_str,
                import_name=import_name,
            )

        case {"from" : address_str, "import": import_val, "as": as_name}:
            return FromImportOneAs(
                address_string=address_str,
                import_name=import_val,
                as_name=as_name,
            )
        
        case {"import" : address_str, "as": as_name}:
            return ImportAs(
                address_string=address_str,
                as_name=as_name,
            )
            
        case {"import": address_str}:
            return Import(address_string=address_str) 
        
        
        
        
            
        case _:
            raise ValueError(f"Invalid import definition: {import_dict}")
    