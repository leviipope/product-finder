import time
import sys

def loading_bar(total=30, duration=5):
    for i in range(total + 1):
        percent = (i / total) * 100
        bar = "█" * i + "-" * (total - i)
        sys.stdout.write(f"\r[{bar}] {percent:6.2f}%")
        sys.stdout.flush()
        time.sleep(duration / total)
    sys.stdout.write("\nDone!\n")

# Example: 30 steps, runs for 5 seconds
loading_bar()
