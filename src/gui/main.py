import login 
from threading import Thread

Thread(target=login.start).start()

while True:
    print("WORK\n")
