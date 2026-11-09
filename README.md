# Pencil motion · עיפרון בתנועה

A micro:bit on a pencil records how the pencil moves over a working day. The recordings are turned into visual maps of the *character* of the movement, not a reconstruction of what was drawn.

## Live pages (GitHub Pages)

- **rings.html**: the main piece. Every work session is a spiral (like tree rings), and the quiet time between sessions is a straight line to the next spiral. It plays the whole day in about 2 minutes. **day overview** (top right) turns into a top-down map; click a ring to fly to it, Esc to go back. When the film is paused (space / ▶) or has reached its end, you can also drag, zoom and click rings freely; pressing play returns to the moving camera.
- **spiral.html**: the first sketch, one continuous flat spiral per recording.

In the day overview two buttons switch the map layout: **עמודות** (columns, the default) and **גל** (wave: left to right, wandering up and down). They appear only in the overview.
URL options for rings.html: `?bg=light` (white background, dark is the default), `?layout=columns|wave`, `?file=pencil_YYYY-MM-DD.csv`.
The background button at the bottom left is invisible on purpose (still clickable). Depth blur is fixed at "gentle" (aperture 0.00022) and has no button.

## Presenting the measuring spiral live

Double-click **`live.command`** in Finder (V1 on the cable, V2 on the pencil with its battery). It starts the recorder and a local web server, then opens `http://localhost:8766/spiral.html`. The spiral redraws every 5 seconds as you draw. Ctrl+C or closing the window stops everything, and the recording is saved. The live view only works on this Mac; the GitHub Pages copy shows the saved recordings.

## Hardware

| | Program | Role |
|---|---|---|
| micro:bit **V2** (on the pencil, battery pack) | `pencil_V2.js` | samples 50×/s: accelerometer x,y,z + sound level, sends by radio (group 73) |
| micro:bit **V1** (USB cable to the Mac) | `receiver_V1.js` | receives radio packets, writes them as text lines to USB, adds radio signal strength |

Flash with makecode.microbit.org → JavaScript tab → paste → Download.

## Recording

```bash
caffeinate -i python3 logger.py
```

- One file per day: `data/pencil_YYYY-MM-DD.csv`. Stopping and resuming the same day appends to it, and the time in between counts as "dead time".
- Columns: `pc_time, mb_ms, ax, ay, az, sound, rssi`.
- Reconnects by itself if the V1 drops off USB. Force-ejects the MICROBIT drive, because Spotlight gets stuck on it and freezes Finder and Photoshop.
- Keeps `data/index.json` up to date. The pages use it to find recordings, since GitHub Pages has no folder listing.
- Mark segments: `python3 mark.py start "סקיצות"` / `python3 mark.py end "סקיצות"` → `data/marks_YYYY-MM-DD.csv`.

## rings.html: main settings (`CFG` at the top of the script)

| Setting | Value | Why |
|---|---|---|
| `QUIET` | 30 s | silence that ends a session |
| `PLAY_SECONDS` | 120 | whole day in ~2 minutes |
| `MIN_DWELL` | 1.5 s | very short sessions still stay on screen long enough to read |
| `SEC_PER_TURN` | 45 s | one spiral turn per 45 s; density depends only on session length |
| `TREMBLE` | 0.24 | trembling = movement irregularity + scratch sound, same size in every ring (no longer tied to density) |
| `SPEED_CM_S` | 4 | rough pencil-tip speed for the distance estimate (Jaffa → Jerusalem = 54 km) |
| `SKETCH` | ~12:00, ~14:00, ~15:30 | time windows coloured blue/violet; marks named "סקיצות" also count |

Colours: blue / violet-pink = sketches, orange / red = texts & thoughts (the choice between the two in each group is random), depth of tone = movement strength.

Earlier versions are in `versions/` (e.g. `rings_v3_before-tremble-change.html`).

## Local preview

`python3 -m http.server 8765` from the parent folder → `http://localhost:8765/pencil-motion/rings.html`.
