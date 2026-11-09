// ===== תוכנית "מקלט" — לצרוב על ה-micro:bit V1 =====
// מקבלת את החבילות מהעיפרון ברדיו ומעבירה אותן למחשב בכבל.
// מוסיפה עמודה: עוצמת אות הרדיו (rssi) — רמז גס למרחק העיפרון מהמקלט.

radio.setGroup(73)              // אותו ערוץ כמו בעיפרון
serial.setTxBufferSize(254)     // גרסה 2: באפר שליחה גדול — ב-50 שורות בשנייה הבאפר הקטן איבד תווים
basic.showIcon(IconNames.Heart)
basic.pause(800)
basic.clearScreen()

let n = 0

radio.onReceivedBuffer(function (buf) {
    let t = buf.getNumber(NumberFormat.UInt32LE, 0)
    let ax = buf.getNumber(NumberFormat.Int16LE, 4)
    let ay = buf.getNumber(NumberFormat.Int16LE, 6)
    let az = buf.getNumber(NumberFormat.Int16LE, 8)
    let sound = buf.getNumber(NumberFormat.Int16LE, 10)
    let rssi = radio.receivedPacket(RadioPacketProperty.SignalStrength)

    serial.writeLine(t + "," + ax + "," + ay + "," + az + "," + sound + "," + rssi)

    // נקודה מהבהבת = מגיעים נתונים
    n += 1
    if (n % 25 == 0) led.toggle(2, 2)
})
