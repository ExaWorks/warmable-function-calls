# Functions with a "Loadable" State

Short version: Break initialization into a separate function that you can run separately and cache.

```python
from functools import lru_cache

@lru_cache()
def initialize(config):
    # ...
    return state

def function(config, x):
    state = initialize(config)
    return f(state, x) 
```

See [`caching-initialization.ipynb`](caching-initialization.ipynb) for an explanation of how this works.
