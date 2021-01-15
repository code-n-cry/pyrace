def rand(arg1: int, arg2: int):
    numb = __import__("random").randint(arg1, arg2)
    if (numb <= arg2/2):
        return True
    else: 
        return False
for _ in range(5):
    print(rand(1,100))