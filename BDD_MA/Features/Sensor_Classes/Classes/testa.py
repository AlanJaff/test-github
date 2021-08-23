import time

TimeCounter = 5
startTime = time.monotonic()
for seconds in range(1, TimeCounter + 1):
    print()  # print a blank line
    time.sleep(1)
    # print(round(startTime))
    # print(round(time.monotonic()))

    print(round(time.monotonic() - startTime), "seconds elapsed")  # print the current elapsed seconds
    # print(int(round(time.monotonic())), "seconds elapsed")  # print the current elapsed seconds
