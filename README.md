# telog

A ready-to-go wrapper for the python logging module with a focus on filtering. 

### Overview
The file `config.yaml` gets loaded into `logging.config.dictConfig` by `telog.py`. The entry for `filename` within this dict config is set by `telog.py` to make sure that log files will always end up in `telog/logs` no matter where the logger is called from. This is key to the philosophy that everything having to do with logging should live within the `telog` directory. Filters are added to this logger using the `filter.yaml` file also in the root of the `telog` directory.

Telog is designed to be added to your project as a git submodule. 

### Levels
For simplicity, this module is concerned with only the log levels of `DEBUG`, `INFO`, `WARN` and `ERROR`. To use other levels modifications must be made to this code.

#### On `DEBUG`
Messages with the `DEBUG` level should only be used when working on a specific problem, and shouldn't become permanent fixtures of the codebase.
 

## Installing

In your project's git directory:

```
git submodule add https://github.com/esologic/telog
```

And run the `setup.py` file and you should be good to go!


## Filtering

The filter is configured using `filter.yaml`. The basic synyax is as follows:

```
filter_in: True/False

modules:
    module1_name:
        function1_name: level1
        function2_name: level2
        function3_name: level3
    module2_name: level4

```
 
If `filter_in` is set to `False`, all messages with levels greater and including the level specified will be removed.

If `filter_in` is set to `True`, all messages with levels less than and including the level specified will be shown.  

For every module under `modules:`, if a `function_name` is listed under it, that corresponding level will be filtered with. If no functions are listed under the module, it's corresponding level will be filtered with.

This is much clearer with examples. 

## Examples:

```
from telog.telog import telogger

class my_class():
    def my_function():
        telogger.info("my message")

    def eat_tide_pod():
        telogger.info("no")

class other_class():
   def other_function():
        telogger.info("my other message")
        
   def foobar():
        telogger.info("foobar message")

class third_class():
    def third_function():
        telogger.info("this is the third message")
```


### Example 1:

We want to filter out ALL messages from `my_class()`:

```
filter_in: False

modules:
    my_class: ERROR
```

### Example 2:
Filter out `my_class.eat_tide_pod`, and `other_class.foobar`:

```
filter_in: False

modules:
    my_class:
        eat_tide_pod: ERROR
    other_class:
        foobar: ERROR
```

### Example 2:
We want to filter in all messages from the `third_class` and `other_class.foobar`

```
filter_in: True

modules:
    other_class:
        foobar: DEBUG
    third_class: DEBUG
```

