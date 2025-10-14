import sys
import time

def loading_bar(total, duration):
    for i in range(total + 1):
        percent = (i / total) * 100
        bar = "█" * i + "-" * (total - i)
        sys.stdout.write(f"\r[{bar}] {percent:6.2f}%")
        sys.stdout.flush()
        time.sleep(duration / total)
    sys.stdout.write("\n")