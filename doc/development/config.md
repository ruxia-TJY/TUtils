# Config

## Overview

config file will be created in `~/.tutils/config.yaml` when first run, and you can edit it to change the configuration of TUtils.

The program reads the configuration file each time it runs.

## Content

Configuration files are saved in YAML format. Example content:

```yaml
app_name: TUtils
app_version: 0.1.0
debug: false
log_level: INFO
use_color: true
verbose: false
repository:
- path: /home/jared/.tutils/Scripts
  type: local
  link: https://github.com/tutils/tutils/index.yaml
custom: {}
```

+ `repository`: the repository list, each repository is a dict with `path` `type` and `link`
    + `path`: the local path of repository
    + `type`: the type of repository, now support `local` and `web`, if `web`,run command-line `repository update` while download to local `path`
    + `link`: the link of repository, if type is `web`, it must be set