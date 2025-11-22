#the libraries that enable communication with the pico and also manipulate time
from machine import Pin, PWM
import time

pwm = PWM(Pin(0), freq=50, duty_u16=8192)
pwm.duty_u16(32768)

# You should not modify the signature (name, input, return type) of this function
def translate(angle: float) -> int:
    """
    Converts an angle in degrees to the corresponding input
    for the duty_u16 method of the servo class
    See https://docs.micropython.org/en/latest/library/machine.PWM.html for more
    details on the duty_u16 method
    """
    #creating a PWM object to control the servo motor
    servo = PWM(Pin(0))
    servo.freq(50)
    
    #the minimum and maximum that can be sent to the duty_u16 method without damaging the servo motor
    duty_min = 1638
    duty_max = 8192
    duty_cycle_value = int(duty_min + (duty_max - duty_min) * angle / 180)
    
    pulse_width = 500 + (2500 - 500) * angle / 180
    duty_cycle = pulse_width / 20000
    duty_cycle_value = int(duty_cycle * 65535)
    servo.duty_u16(duty_cycle_value) #maybe/or servo.duty_u16(translate(45))
    print("duty_cycle_value =" , duty_cycle_value)

    return duty_cycle_value #to return the value of the duty cycle 

translate(90) #calling the function