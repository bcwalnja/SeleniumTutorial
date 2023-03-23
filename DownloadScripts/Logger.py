import time

def log(m):
    try:
        t = time.localtime()
        c = time.strftime("%Y-%m-%d %H:%M:%S", t)
        
        if isinstance(m, Exception):
            errorMessage = "An error of type {} occurred.".format(type(m).__name__)
            print("{} {}".format(c, errorMessage))
        else:
            print("{} {}".format(c, str(m)))
    except:
        pass