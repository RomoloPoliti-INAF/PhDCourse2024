from rich import print
from functools import wraps

def decor(funct):
    @wraps(funct)
    def wrapper(*args, **kwargs):
        print("[yellow]##################################[/yellow]")
        a=funct(*args, **kwargs)
        print("[yellow]##################################[/yellow]")
        return a
    return wrapper

@decor
def mean(numbers: list)->float:
    """Compute the mean of a list of numbers"""
    print("Computing mean...")
    return sum(numbers) / len(numbers)




