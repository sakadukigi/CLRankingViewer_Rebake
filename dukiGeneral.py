import os

def TryMakeDir(path:str) -> bool:
    if os.path.isdir(path):
        os.mkdir(path)
        return True
    else:
        return False

if __name__=="main":
    pass