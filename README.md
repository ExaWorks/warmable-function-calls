# Warmable Function Calls

Many tasks in workflows require a expensive "initialization" steps that, once performed, can be used across multiple tasks.
For example, you may want to reuse a machine learning model for multiple interface tasks but want to avoid loading it onto GPUs more than once.
We show a few Python examples of how to avoid repeating these costly initializations in ways that work with many workflow systems.

## First, some background on workflow engines and Python

Workflow systems usually run functions on Python interpreters running on the remote compute node.
Each worker receives a function and its inputs as a serialized (e.g., pickled) message that the it then deserializes and executes.
The worker then sends the outputs back to the rest of the system and downloads another function/inputs to run.
_The worker typically stays alive between function calls_.
Our goal is write functions which cache their initialization data in memory of that worker.

Python offers several methods for variables that stay resident between calls.
The [`globals`](https://docs.python.org/3/library/functions.html#globals) function that gives you free rein to manipulate globals that are visible anywhere and always, but that gives enough freedom to cause hard-to-debug errors.
Rather, we'll use ["module-level" globals](https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules) to have a safer route to persistent memory.

Module-level globals rely on Python allowing for non more than one copy of a module to exist in memory. 
Any code that interacts with that module will get the same functions and same values that are part of the module.
Any code that changes one of those values changes it everywhere, including functions that are part of the module.

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

We will use this mechanism a few different ways to preserve expensive-to-get state between calls.

> Note: See [`demonstrate-globals.ipynb`](./demonstrate_globals.ipynb) for a live demonstration.
