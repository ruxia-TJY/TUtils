# AddScript



## code structure

you must do like this

```python
import the_library_you_want_name

# the rules must be have
# rules for command Arguments
rules = {
	"rules_name":{
		"type":"rules_type",
		"rules":"Arguments_mode",
		"value":"target_value"
	}	
}


# main function, the script run from this
# cmd is rules after parse.
# such as
# rules = {
#	"path":{
#	  "type":"str"
#     "rules":1,
#     "value":"C:/"
#	}
# }
# and the command is 
# D:/
# you can get with cmd["path"]["value"] , the value is "D:/" in string type
def main(cmd:str):
    your_code
```

**Example**

```python
import os
from rich.console import Console
console = Console()

rules = {
    "path": {
        'type':'str',
        'rules': 1,
        'value':None
    },
    "hide":{
        "type":"bool",
        "rules":"?",
        "value":False
    }
}


def main(cmd:dict):
    path = cmd['path']['value'][0]

    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')

    fileCount = 0
    dirCount = 0

    if cmd['hide']['value']:
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                dirCount += 1
                console.print(os.path.join(root, dir),style='bold yellow')

            for file in files:
                fileCount += 1
                console.print(os.path.join(root, file),style='#af00ff')
    else:
        for root, dirs, files in os.walk(path):
            dirCount += len(dirs)
            fileCount += len(files)

    console.rule()
    console.print(f'Files Count:{fileCount}',style='bold green')
    console.print(f'Dirs Count:{dirCount}',style='bold green')
    console.print(f'Total Files:{fileCount + dirCount}',style='bold green')
```



## rules

rules is a dict , every argument rules has three key-value `type``rules``value`

### rules type

type is the type of this argument,such `str` is `string` ,`bool` is `bool`

+ `bool`
+ `int`
+ `float`
+ `str`


### rules rules

+ `?` the argument has 0 or 1
+ `number` the number of the argument must have，it will set as list in `value`
+ `*` zero or more

### rules value

the value of this argument, type is in key `type`

## main

your scrpit start from here, the param cmd is dict,value is `rules` with the value in command write