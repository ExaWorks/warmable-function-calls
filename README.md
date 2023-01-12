# Warmable Function Calls

Many tasks in workflows require a expensive "initialization" steps that, once performed, can be used across successive invocations for that task.
For example, you may want to reuse a machine learning model for multiple interface tasks and avoid loading it onto GPUs more than once.
We show a few Python examples of how to avoid repeating costly initializations in ways that work with many workflow systems.

## First, some background on workflow engines and Python

Workflow systems run functions on Python workers running on remote computers.
Each worker receives a function and its inputs as a serialized (e.g., pickled) message that it then deserializes, executes, and sends the result back.
_The worker often stays alive between calls,_ which prevents loading libraries more than once.
We can leverage the persistence to make "warmable" functions by keeping any initialization data in memory.

Python offers several methods for variables that stay resident between calls.
The [`globals`](https://docs.python.org/3/library/functions.html#globals) function that gives you free rein to manipulate globals that are visible anywhere and always, but that gives enough freedom to cause hard-to-debug errors.
Rather, we'll use ["module-level" globals](https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules) to have a safer route to persistent memory.

Module-level globals rely on Python loading at most one copy of a module.
Any code that interacts with that module will get the same functions and same values that are part of the module.
Any code that changes one of those values changes it everywhere, including in functions that are part of the module.

For example, we can create a module file (named `module.py`) with a single global

```python

count = 0

def increase_count() -> int:
    """Increase the count and return the new value
    
    Returns:
        New value
    """
    global count
    count += 1
    return count
```

The global, `count`, can be altered by the function call and is re-used between calls.

```python

from module import increase_count

print(increase_count()) # Returns 1
print(increase_count()) # Returns 2 because the first call changed the global
```

We will use this mechanism a few different ways to preserve expensive-to-get state between calls. See [`demonstrate-globals.ipynb`](./demonstrate-globals.ipynb) for a live demonstration.

These globals have a few limitations.
For one, they do not stay if the worker process is restarted.
Some workflow tools (e.g., [Work Queue](https://cctools.readthedocs.io/en/latest/work_queue/)) restart the worker between function calls to avoid interference between tasks and Python's [`ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor) lets us configure whether to keep workers alive.
Multiple workers on the same node will also have to initialize themselves because they do not share memory (in most cases).
Beyond these limitations, the techniques described here work with many kinds of workflow systems.

## Some other ground-work

You will need to make your function part of a Python module to make it warmable.
Creating a module can be as easy as just creating a ".py" file and then ensuring that it is on your path,
such as by putting it in the same directory you run Python or altering the Python Path so that your .py file can be found.
See [Python's documentation](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#) or [Setuptool's quickstart](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#) to learn more.


## A variety of approaches

There are a few different ways we can exploit these "persistent" variables to create warmable function calls.
They are (ordered roughly by complexity):

1. [*Storing state as a global*](./global-state/README.md): Useful for when functions have state which only need be loaded in once.
1. [*Launching an external process.*](./external-process/README.md): If your function invokes an external code and you can modify that code to stay alive between calls.
