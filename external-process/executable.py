"""An example function that runs a science code on inputs received from standard in

It will exit if no input data is received past a certain timeout or if the stdin starts reading only empty strings,
which means that it has closed.
"""
from selectors import DefaultSelector, EVENT_READ
from typing import TextIO
from pathlib import Path
from time import sleep
import json
import sys
from typing import Optional, Iterator


def read_inputs(pipe, timeout: float = 5) -> Iterator[Optional[dict]]:
    """Read inputs from a pipe until a termination condition is met

    Args:
        timeout: Timeout in seconds
    Yields:
        Input arguments or ``None`` if there are no more inputs
    """

    # We use a Selector to wait for inputs from stdin
    #  See: https://docs.python.org/3/library/selectors.html#selectors.DefaultSelector
    sel = DefaultSelector()
    sel.register(pipe, EVENT_READ)  # Wait to read from stdin
    
    # Loop until end is reached
    while True:

        # Blocks until pipe is ready to read or a timeout has passed
        events = sel.select(timeout=timeout)

        # Break if pipe is not ready, which appears as an empty "events"
        if len(events) == 0:
            return

        # If the file is closed, then it will always read a blank message. Exit if this happens
        msg = pipe.readline()
        if len(msg) == 0:
            return

        # Yield the path
        yield json.loads(msg[:-1])  # Last character is a newline

    
def function(x: float) -> float:
    return x + 1


if __name__ == "__main__":
    """Receives path to inputs via stdin"""

    sleep(5)  # Emulate a large startup cost

    # Create a generator that produces
    input_generator = read_inputs(sys.stdin)

    # Loop until either we receive data or the timeout occurs
    for inputs in input_generator:
        # Run the computation
        y = function(*inputs['args'], **inputs['kwargs'])

        # Return the result
        print(json.dumps(y), flush=True)
