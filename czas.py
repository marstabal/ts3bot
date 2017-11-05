import time
import stale

def delay():
    time.sleep(stale.STD_DELAY)

def delay_long():
    time.sleep(stale.LONG_DELAY)
    
def delay_by(timeout):
    time.sleep(timeout)
    
MS = 0.001
SEK = 1.0
MIN = 60.0
GODZ = 3600.0
DZIEN = 24 * 3600.0