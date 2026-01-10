from dataclasses import dataclass
from pathlib import Path
from typing import  Optional, Protocol


class BaseImport(Protocol):
    path : Path 
    
    def resolve_path(self, base_path: Optional[Path] = None ) -> Path:
        if base_path is None:
            return self.path.resolve()
        
        if self.path.is_absolute():
            return self.path.resolve()
        
        return (base_path.parent / self.path).resolve()
    
@dataclass
class Import(BaseImport):
    path : Path

@dataclass
class ImportAs(BaseImport):
    path : Path
    as_name : str

@dataclass
class FromImportOne(BaseImport):
    path : Path
    import_name : str
    
@dataclass
class FromImportOneAs(BaseImport):
    path : Path
    import_name : str
    as_name : str

@dataclass
class FromImportMany(BaseImport):
    path : Path
    import_names : list[str]
    

@dataclass
class FromImportStar(BaseImport):
    path : Path
    

def detect_import(import_dict: dict) -> BaseImport:
    
    if set(import_dict.keys()) == {"import"}:
        return Import(path=Path(import_dict["import"]))
    
    if set(import_dict.keys()) == {"import", "as"}:
        return ImportAs(path=Path(import_dict["import"]), as_name=import_dict["as"])


    if set(import_dict.keys()) == {"from", "import"} and isinstance(import_dict["import"], str) and  import_dict["import"] == "*":
        return FromImportStar(path=Path(import_dict["from"]))

    
    if set(import_dict.keys()) == {"from", "import"} and isinstance(import_dict["import"], str):
        return FromImportOne(path=Path(import_dict["from"]), import_name=import_dict["import"])
    
    if set(import_dict.keys()) == {"from", "import"} and isinstance(import_dict["import"], list):
        return FromImportMany(path=Path(import_dict["from"]), import_names=import_dict["import"])
    
    if set(import_dict.keys()) == {"from", "import", "as"}:
        return FromImportOneAs(path=Path(import_dict["from"]), import_name=import_dict["import"], as_name=import_dict["as"])
    
    raise ValueError(f"Invalid import definition: {import_dict}")

