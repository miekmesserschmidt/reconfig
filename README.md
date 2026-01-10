
Reconfig is a configuration management tool for TOML. It includes a recursive import mechanism so that configurations can be across multiple files. The import syntax is closely modeled on Python's own import syntax. 

It handles relative and absolute imports.

It detects and throws on circular imports.


```TOML
imports = { 
    # simple import  (filename becomes the key)
    { import = "{ ... filepath} ..." },      
    
    # renaming simple import (provided newname becomes the key)
    { import = "{filepath}", as = "{newname}"},
    
    # import a list of variables from file       
    { from = "{filepath}", import = ["{name1}", "{name2}"]}, 
    
    # import a single of variables from file   
    { from = "{filepath}", import = "{name}"},
    
    # import a single of variables from file (provided newname becomes the key)
    { from = "{filepath}", import = "{name}", as = "{newname}"},
    
    # import all top-level elements from file (star import)
    { from = "{filepath}", import = "*" }
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
    {import = "./includes_A/include_a.toml"},
]

[section]
imports = [
    {from = "./includes_A/include_b.toml", import = "var_b"},
    {from = "./includes_A/include_c.toml", import = "var_c", as="new_var_c"},
    {from = "./includes_B/include_d.toml", import = ["var_d", "section_d"]},
    {from = "./includes_B/include_e.toml", import = "*"}
]

####
# ./includes_A/include_a.toml
####
imports = [ 
    {import = "../includes_B/include_d.toml"},
    {import = "/etc/reconf/etc_conf.toml"}
]

var_a = "value_a"

####
# ./includes_A/include_b.toml
####
var_b = "value_b"

[section_in_b]
var_in_section_b = "value_in_section_b"

####
# ./includes_A/include_c.toml
####
var_c = "value_c"
var_d = "value_d"

####
# ./includes_B/include_d.toml
####
var_d = "value_d_yes"

[section_d]
section_d_var_d = "section_d_value_d" 

[section_e]
var_section_e = "not present"

####
# ./includes_B/include_e.toml
####
[db]
host = "localhost"
port = 5432

[cache]
host = "redis.local"
ttl = 3600

####
# /etc/reconf/etc_conf.toml
####
etc_var = "etc"
```

```python

from reconfig import resolve_config
from pathlib import Path

result = resolve_config(Path("./root.toml"))

assert result == {
    "include_a": {
        "include_d": {
            "var_d": "value_d_yes",
            "section_d": {
                "section_d_var_d": "section_d_value_d"
            },
            "section_e": {
                "var_section_e": "not present"
            }
        },
        "etc_conf": {
            "etc_var": "etc"
        },
        "var_a": "value_a"
    },
    "section": {
        "var_b": "value_b",
        "new_var_c": "value_c",
        "var_d": "value_d_yes",
        "section_d": {
            "section_d_var_d": "section_d_value_d"
        },
        "db": {
            "host": "localhost",
            "port": 5432
        },
        "cache": {
            "host": "redis.local",
            "ttl": 3600
        }
    }
}

```