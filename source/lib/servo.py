import RPi.GPIO as GPIO
from time import sleep

MAX_VALUE = 100
MIN_VALUE = 0

SERVO_PIN = 3 # physical pin number

IDLE_ANGLE = 90
current_angle = IDLE_ANGLE


class ServoCam:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        GPIO.setwarnings(False)
        self.pwm = GPIO.PWM(SERVO_PIN, 50) # pwm 50hz
        self.pwm.start(0)


    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()


    def setAngle(self, angle):
        duty = angle/18+2
        GPIO.output(SERVO_PIN, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(SERVO_PIN, False)
        self.pwm.ChangeDutyCycle(0)


