"""Example used to teach module-level globals"""

count = 0

def increase_count() -> int:
    """Increase the count and return the new value
    
    Returns:
        New value
    """
    global count
    count += 1
    return count