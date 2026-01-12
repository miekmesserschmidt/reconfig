
Reconfig is a configuration management tool for TOML. It includes a recursive import mechanism so that configurations can be across multiple files. The import syntax is closely modeled on Python's own import syntax. 

It handles relative and absolute imports.

It detects and throws on circular imports.


Syntax
=====

```TOML
imports = { 
    # simple import  (filename becomes the key)
    { import = "{filepath}" },      
    
    # simple import  (variable/section becomes the key)
    { import = "{filepath}::{variable/section}" },      

    # renaming simple import (provided newname becomes the key)
    { import = "{filepath}", as = "{newname}"},

    # renaming simple import (provided newname becomes the key)
    { import = "{filepath}::{variable/section}", as = "{newname}"},

    # import a list of variables from file       
    { from = "{filepath}", import = ["{name1}", "{name2}"]}, 
    
    # import a list of variables from a section       
    { from = "{filepath}::section", import = ["{name1}", "{name2}"]}, 

    # import a single of variables from file   
    { from = "{filepath}", import = "{name}"},
    
    # import a single of variables from section   
    { from = "{filepath}::{section}", import = "{name}"},

    # import a single of variables from file (provided newname becomes the key)
    { from = "{filepath}", import = "{name}", as = "{newname}"},
    
    # import a single of variables from section (provided newname becomes the key)
    { from = "{filepath}::{section}", import = "{name}", as = "{newname}"},

    # import all top-level elements from file (star import)
    { from = "{filepath}", import = "*" }

    # import all top-level elements from section (star import)
    { from = "{filepath}::{section}", import = "*" }

}

```

Example:
==========

```TOML

####
# ./root.toml
####
#top imports
imports = [
    {import = "./recursive.toml"},
]

[section]
imports = [
    {import = "a.toml::var_a"},
    {import = "a.toml::section_a.sub_section_a.sub_sec_var"},
    {import = "a.toml", as = "a_renamed"},
    { from = "b.toml", import = "var_b"},
    { from = "b.toml::section_b", import = "sec_val_b"},
    { from = "b.toml::section_b", import = "sec_val_b", as = "renamed_sec_val_b"},
    { from = "c.toml", import = "*"},
    { from = "c.toml::section_c", import = ["section_var_c0", "section_var_c2"]},    
 ]

####
# ./recursive.toml
####
imports = [ 
    {import = "a.toml"},
    {import = "b.toml"},
    {import = "c.toml"}
]

####
# ./a.toml
####
var_a = "val_a"

[section_a.sub_section_a]
sub_sec_var = "sub_sec_value"


####
# ./c.toml
####
var_b = "val_b"
[section_b]
section_var_b = "sec_val_b"

####
# ./c.toml
####
var_c = "val_c"
[section_c]
section_var_c0 = "sec_val_c0"
section_var_c1 = "sec_val_c1"
section_var_c2 = "sec_val_c2"

```

```python

from reconfig import resolve_config
from pathlib import Path

result = resolve_config(Path("./root.toml"))

expected = {
        "recursive": {
            "a": {"var_a": "val_a", "section_a": {"sub_section_a": {"sub_sec_var": "sub_sec_value"}}},
            "b": {"var_b": "val_b", "section_b": {"sec_val_b": "sec_val_b"}},
            "c": {
                "var_c": "val_c",
                "section_c": {
                    "section_var_c0": "sec_val_c0",
                    "section_var_c1": "sec_val_c1",
                    "section_var_c2": "sec_val_c2",
                },
            },
        },
        "section": {
            "var_a": "val_a",
            "sub_sec_var" : "sub_sec_value",
            "a_renamed": {"var_a": "val_a", "section_a": {"sub_section_a": {"sub_sec_var": "sub_sec_value"}}},
            "var_b": "val_b",
            "sec_val_b": "sec_val_b",
            "renamed_sec_val_b": "sec_val_b",
            "var_c": "val_c",
            "section_c": {
                "section_var_c0": "sec_val_c0",
                "section_var_c1": "sec_val_c1",
                "section_var_c2": "sec_val_c2",
            },
            "section_var_c0": "sec_val_c0",
            "section_var_c2": "sec_val_c2",
        },
    }

assert result == expected

```