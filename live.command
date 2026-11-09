#!/bin/bash
# Live measuring spiral — double-click in Finder (or run in a terminal) to present it live.
# Needs: V1 on the USB cable, V2 on the pencil with its battery.
# Starts a small local web server + the recorder, and opens the live spiral in the browser.
# Ctrl+C (or closing this window) stops everything; the recording is saved.
cd "$(dirname "$0")"
python3 -m http.server 8766 >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null' EXIT
( sleep 6; ${OPEN:-open} "http://localhost:8766/spiral.html" ) &   # after the recorder registered today's file
caffeinate -i python3 logger.py
