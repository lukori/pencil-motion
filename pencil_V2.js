// ===== תוכנית "עיפרון" — לצרוב על ה-micro:bit V2 =====
// דוגמת 50 פעמים בשנייה (כל 20ms) בקצב קבוע: אקסלרומטר (x,y,z) ורמת קול.
// שולחת כל דגימה גם בכבל (Serial) וגם ברדיו למקלט.
// גרסה 2: במקום basic.forever + pause (שהוסיפו השהיות) — לולאה עם תזמון מדויק.

radio.setGroup(73)              // "ערוץ" — חייב להיות זהה במקלט
radio.setTransmitPower(7)       // עוצמת שידור מקסימלית
input.setAccelerometerRange(AcceleratorRange.FourG)

basic.showIcon(IconNames.Yes)
basic.pause(1000)
basic.clearScreen()

let PERIOD = 20                 // מילישניות בין דגימות (20 = 50 בשנייה)
let buf = pins.createBuffer(12)
let n = 0

control.inBackground(function () {
    let next = input.runningTime()
    while (true) {
        let t = input.runningTime()
        let ax = input.acceleration(Dimension.X)
        let ay = input.acceleration(Dimension.Y)
        let az = input.acceleration(Dimension.Z)
        let sound = input.soundLevel()

        // רדיו: אורזים את המספרים לחבילה קטנה
        buf.setNumber(NumberFormat.UInt32LE, 0, t)
        buf.setNumber(NumberFormat.Int16LE, 4, ax)
        buf.setNumber(NumberFormat.Int16LE, 6, ay)
        buf.setNumber(NumberFormat.Int16LE, 8, az)
        buf.setNumber(NumberFormat.Int16LE, 10, sound)
        radio.sendBuffer(buf)

        // כבל: שורת טקסט אחת לכל דגימה
        serial.writeLine(t + "," + ax + "," + ay + "," + az + "," + sound + ",")

        // נקודה מהבהבת פעם בשנייה = "אני חי"
        n += 1
        if (n % 50 == 0) led.toggle(2, 2)

        // מחכים בדיוק עד הדגימה הבאה
        next += PERIOD
        let wait = next - input.runningTime()
        if (wait > 0) {
            basic.pause(wait)
        } else {
            next = input.runningTime()   // נפלנו מאחור — מתחילים לספור מחדש
            basic.pause(1)
        }
    }
})
