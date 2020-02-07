from time import sleep


def login_dec(auth):
        try:
            if auth:
               return  True
            elif not auth:
                return False
        except:
            return False

for i in range(10):
    print("hello")
    sleep(2)