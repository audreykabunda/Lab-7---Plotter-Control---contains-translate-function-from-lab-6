# the libraries that enable communication with the pico and also manipulate time
from machine import Pin, PWM
import time

pwm = PWM(Pin(0), freq=50, duty_u16=8192)
pwm.duty_u16(32768)

# you can change this value after calibrating your plotter jig
ANGLE_OFFSET = 0     # try values like -10, +5, +12 to calibrate each servo

#setting PWM values for the servos
shoulder = PWM(Pin(0), freq=50)
elbow = PWM(Pin(1), freq=50)
wrist = PWM(Pin(2), freq=50)

# You should not modify the signature (name, input, return type) of this function
def translate(angle: float) -> int:
    """
    Converts an angle in degrees to the corresponding input
    for the duty_u16 method of the servo class.
    This prevents sending unsafe PWM values to the servo.
    """

    # apply the offset to the input angle
    adjusted_angle = angle + ANGLE_OFFSET

    # clamp the adjusted angle so it stays within safe bounds
    if adjusted_angle < 0:
        adjusted_angle = 0
    if adjusted_angle > 180:
        adjusted_angle = 180

    # the minimum and maximum pulse widths (in microseconds)
    # that correspond to the servo's physical limits
    pulse_min = 500     # 0 degrees
    pulse_max = 2500    # 180 degrees

    # calculate the pulse width for the given angle
    pulse_width = pulse_min + (pulse_max - pulse_min) * (adjusted_angle / 180)

    # the period of a 50 Hz PWM signal is 20,000 microseconds
    duty_cycle = pulse_width / 20000

    # convert the duty cycle (0.0–1.0) into a 16-bit value for duty_u16
    duty_cycle_value = int(duty_cycle * 65535)

    print("angle =", angle, "adjusted_angle =", adjusted_angle, 
          "duty_cycle_value =", duty_cycle_value)

    # return this value to be used by servo.duty_u16(...)
    return duty_cycle_value

#setting functions to control the movement of the pen servo
def wrist_up():
    wrist.duty_u16(translate(0))
    time.sleep(0.5)
def wrist_down():
    wrist.duty_u16(translate(30))
    time.sleep(0.5)

def move_to(x, y):
    """
    Move the shoulder and elbow servos to approximate x,y position.
    For beginners, we just map X -> shoulder angle, Y -> elbow angle.
    """
    shoulder_angle = x
    elbow_angle = y

    #moving the servos
    shoulder.duty_u16(translate(shoulder_angle))
    elbow.duty_u16(translate(elbow_angle))
    time.sleep(0.05)

def run_gcode(filename):
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line == "" or line.startswith(";"):
                continue

            #wrist up and down
            if line.startswith("M3"):
                wrist_down()
                continue
            if line.startswith("M5"):
                wrist_up()
                continue

            # MOVE commands (use S and E as X and Y)
            if line.startswith("G1"):
                x = None
                y = None
                for part in line.split():
                    if part.startswith("S"):
                        x = float(part[1:])
                    elif part.startswith("E"):
                        y = float(part[1:])
                if x is not None and y is not None:
                    move_to(x, y)
    print("Finished drawing!")

wrist_up()
time.sleep(1)

run_gcode("circle.gcode") # type: ignore