import time
from chatapp.windowgui.timers import RealTimer


t = RealTimer()
print("now")
print(time.monotonic())
t.start()
while not t.passed(.1):
    pass
print(time.monotonic())

print("gochat")
