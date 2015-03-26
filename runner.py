import pyreally
import logging
import time

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    try:
        really = pyreally.Really()
        really.login_anonymous()
        f = really.get("/users/5976233945367449600")
        print("I got a future: %s" % f)
        print("The result is: %s" % f.result())
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT, Closing REALLY")
        really.close()
    except pyreally.OperationError as e:
        print("OPERATION FAILED %s" % e)
        time.sleep(10)
        really.close()