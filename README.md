# HiQClick | HiQCom

Script was written to create from 'HqDev QA automation' '**Lazy** HqDev QA automation'

## Commands
```
Usage: cp.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dcd    Shutting docker containers for [hipanel, hiapi, hiam] down  
  dcm    Migrates database for [hiapi]  
  dcu    Running docker containers for [hipanel, hiapi, hiam] up  
  run    runs a test  
  setup  sets .env variables  

```

2 commands need attention:  

> ./cp.py run ToggleSign

### Command `run`:
1. Format test name to `TestNameCest.php`. You can use format
   1. TestName
   2. TestNameCest
   3. TestNameCest.php

2. Search for test in all modules
3. Finally, run it

### Command `setup`

This command is responsible to init .env variables:  

*all variables gets absolute path*  

1. `BASH_DIR` - folder where are all `.sh` files  
2. `WORK_DIR` - folder where are hipanel, hiapi, hiam dirs are
3. `PREFIX` - prefix for hiapi, hipanel, hiam
4. `HIAPI_DIR` - ...
5. `HIAPANEL_DIR` - ...

## Annotation 

* For best performance place dir with script in potential `WORK_DIR`(see [command `setup`](#command-setup)
* Can be created alias
  * your_custom_command = absolute_path_to_script  
  >hq run ToggleSign
  * and use it in any dir, cos script working with absolute path although
  
---
* This script probably(well, I'm sure) has a lot of bugs. But I'm working on it.
* This script can be improved for sure, and this is my target too
