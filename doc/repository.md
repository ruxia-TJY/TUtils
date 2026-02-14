# Repository

the repository dir:
```
├── index.yaml
└── example dir 1
    ├── example code file.py
    └── index.yaml
```


### Repository index.yaml

example:
```yaml
name: File
scripts:
  - Z2V0RmlsZUNvdW50
  - WDdadawdwadsadad
```

+ `name`: the name of repository
+ `scripts`: the list of script in repository, just folder name,not script name

### script index.yaml

example:
```yaml
name: Z2V0RmlsZUNvdW50
version: 0.0.1
description: get current folder repository count
author: Jared3Dev
email: ruxia.tjy@qq.com
run: getfilecount.py
src:
  - getfilecount.py
license: MIT
````

+ `name`: the name of script
+ `version`: the version of script
+ `description`: the description of script
+ `author`: the author of script
+ `email`: the email of author
+ `run`: the file name of script to run, must in src list
+ `src`: the list of file name of script, just file name,not path
+ `license`: the license of script
