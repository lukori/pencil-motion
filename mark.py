"""
סימון קטעים בהקלטה. כל סימון נכתב לקובץ data/marks_YYYY-MM-DD.csv
שימוש:
    python3 mark.py start "סקיצות"     ← תחילת קטע
    python3 mark.py end "סקיצות"       ← סוף קטע
"""
import os, sys
from datetime import datetime

event, label = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
now = datetime.now()
path = os.path.join(here, "data", now.strftime("marks_%Y-%m-%d.csv"))
new = not os.path.exists(path)
with open(path, "a") as f:
    if new:
        f.write("pc_time,event,label\n")
    f.write(f"{now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]},{event},{label}\n")
print(f"{event} · {label} · {now.strftime('%H:%M:%S')}")
