"""
מקליט נתונים מה-micro:bit המחובר בכבל לקובץ CSV בתיקייה data/.
הפעלה:   caffeinate -i python3 logger.py
עצירה:   Ctrl+C

- קובץ אחד לכל יום: עצירה והמשכה באותו יום מוסיפות לאותו קובץ.
  הזמן שבין עצירה להמשכה נשאר בקובץ כפער בזמן = "זמן מת".
- אם ה-micro:bit מתנתק (ה-V1 עושה את זה לפעמים) — מחכים שיחזור ומתחברים מחדש לבד.
- כונן MICROBIT מנותק אוטומטית (רק הכונן; ערוץ הנתונים נשאר) — כדי ש-Spotlight
  לא ייתקע עליו ויקפיא את Finder / פוטושופ. כדי לצרוב שוב: לנתק ולחבר את הכבל.
"""
import glob, os, subprocess, time
from datetime import datetime
import serial

HEADER = "pc_time,mb_ms,ax,ay,az,sound,rssi"
stamp = lambda: datetime.now().strftime("%H:%M:%S")


def eject_drive():
    for vol in glob.glob("/Volumes/MICROBIT*"):
        try:  # "force" — כי Spotlight (mds_stores) אוחז בכונן ומונע ניתוק רגיל
            ok = subprocess.run(["diskutil", "unmount", "force", vol],
                                capture_output=True, timeout=15).returncode == 0
        except subprocess.TimeoutExpired:
            ok = False
        print(f"[{stamp()}] כונן {os.path.basename(vol)} נותק" if ok
              else f"[{stamp()}] לא הצלחתי לנתק את {vol} — ממשיכים בכל זאת")


def connect():
    """מחכה עד שיש micro:bit מחובר, מנתק את הכונן, ופותח את ערוץ הנתונים."""
    waiting = False
    while True:
        ports = glob.glob("/dev/cu.usbmodem*")
        if ports:
            time.sleep(1.5)          # נותנים לו רגע להתייצב אחרי חיבור
            eject_drive()
            try:
                ser = serial.Serial(ports[0], 115200, timeout=1)
                print(f"[{stamp()}] מחובר ל-{ports[0]}")
                return ser
            except serial.SerialException:
                pass
        if not waiting:
            print(f"[{stamp()}] אין micro:bit מחובר — מחכה שיחזור...")
            waiting = True
        time.sleep(2)


here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "data"), exist_ok=True)
path = os.path.join(here, "data", datetime.now().strftime("pencil_%Y-%m-%d.csv"))
is_new = not os.path.exists(path)


def write_index():
    """data/index.json — list of recordings, newest last (GitHub Pages has no folder listing)."""
    import json
    files = sorted(glob.glob(os.path.join(here, "data", "pencil_*.csv")), key=os.path.getmtime)
    with open(os.path.join(here, "data", "index.json"), "w") as jf:
        json.dump({"files": [os.path.basename(x) for x in files]}, jf, indent=1)


print(f"{'שומר אל' if is_new else 'ממשיך את'}: {path}")
print("Ctrl+C לעצירה\n")

rows, drops, last_report, last_line = 0, 0, time.time(), ""
ser = connect()

with open(path, "a", buffering=1) as f:
    if is_new:
        f.write(HEADER + "\n")
    write_index()
    try:
        while True:
            try:
                raw = ser.readline().decode("utf-8", errors="ignore").strip()
            except (serial.SerialException, OSError):
                drops += 1
                print(f"[{stamp()}] ה-micro:bit התנתק (פעם {drops}). הנתונים עד עכשיו שמורים.")
                try: ser.close()
                except Exception: pass
                time.sleep(2)
                ser = connect()
                continue
            parts = raw.split(",")
            if len(parts) == 6 and parts[0].isdigit():
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                f.write(now + "," + raw + "\n")
                rows += 1
                last_line = raw
            if time.time() - last_report >= 5:
                print(f"{rows:>8} שורות | אחרונה: {last_line}")
                last_report = time.time()
    except KeyboardInterrupt:
        write_index()
        print(f"\nנעצר. נשמרו {rows} שורות ב-{path} (התנתקויות: {drops})")
