# GitHub User Summary

### Get a summary list group by day via GitHub API

*Only tested under python 3.7.1*

Example:

``` bash
python3 main.py -a BLumia -c 30
```

Usage:

``` bash
    -h          --help            : Display this help
    -a <id>     --account <id>    : GitHub account id
    -c <count>  --count	<count>   : Event count fetched from GitHub (Per page, default: 30, max: 100)
    -p <page>   --page <page>     : N-th page, default is 1
    -o <path>   --output= <path>  : Not implemented...
```
