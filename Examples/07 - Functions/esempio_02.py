def decor(funct):
    """Decoratore"""
    def wrapper(*args, **kwargs):
        """>>> Wrapper <<<<"""
        print("##################################")
        a=funct(*args, **kwargs)
        print("##################################")
        return a
    return wrapper
    


@decor
def test01(name: str, age: int)->str:
    print(f"{name} is {age} years old")
    
@decor
def test02():
    """TEST 02"""
    print("test2")


def test03():
    """TEST 03"""
    print("test3")
