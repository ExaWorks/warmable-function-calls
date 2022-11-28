# Caching a Whole Process

Some functions are expensive because they launch an external code that has a large startup cost.
We show how to modify that external code so that it stays alive and your Python function to know how to connect to it.

The short version:
1. The Python function launches the external code and places links to the standard in and output in a cache
1. The Python function sends inputs (or where to find them) via standard in
1. The external process retrieves inputs
1. The external process sends outputs (or where to find them) via standard out
1. The Python function retrieves outputs

> Note that this method requires heavy modifications on how the external code accepts inputs.

Full details are described in here: [notebook](./explain-subprocessing.ipynb)
