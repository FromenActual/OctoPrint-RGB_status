import RPi.GPIO as GPIO

# Designed to be a drop-in replacement for rpi-ws281x with simple LED strips. Simple means strips with a single high voltage line, and each color is grounded to produce light.
class SimpleLEDStrip:
	def __init__(self, red_pin, green_pin, blue_pin, freq_hz=50, led_invert=False, led_brightness=255):
		# Store values
		self.red_pin = red_pin
		self.green_pin = green_pin
		self.blue_pin = blue_pin
		self.freq_hz = freq_hz
		self.led_invert = led_invert
		self.led_brightness = led_brightness
		
		# Configure pins for output
		setupGPIO()
	
	def setupGPIO(self):
		# GPIO numbering
		GPIO.setmode(GPIO.BCM)
		
		# Output for each pin
		GPIO.setup(self.red_pin, GPIO.OUT)
		GPIO.setup(self.green_pin, GPIO.OUT)
		GPIO.setup(self.blue_pin, GPIO.OUT)
		
		# PWM for each pin
		self.red_pwm = GPIO.PWM(self.red_pin, self.freq_hz)
		self.green_pwm = GPIO.PWM(self.green_pin, self.freq_hz)
		self.blue_pwm = GPIO.PWM(self.blue_pin, self.freq_hz)
	
	def clearGPIO(self):
		# Clean up only the pins used
		GPIO.cleanup(self.red_pin)
		GPIO.cleanup(self.green_pin)
		GPIO.cleanup(self.blue_pin)
	
	def setPixelColorRGB(self, pixelIndex, red, greed, blue):
		# pixelIndex not used, only included for drop-in replacement
		# Rescales each color from 0-255 to 0-100 (duty cycle %), and adjusts for led_brightness
		brightness_conversion = 100/200 * self.led_brightness/255
		
		# Store duty cycles
		self.red_duty_cycle = red * brightness_conversion
		self.green_duty_cycle = green * brightness_conversion
		self.blue_duty_cycle = blue * brightness_conversion
	
	def show(self):
		self.red_pwm.ChangeDutyCycle(self.red_duty_cycle)
		self.green_pwm.ChangeDutyCycle(self.green_duty_cycle)
		self.blue_pwm.ChangeDutyCycle(self.blue_duty_cycle)
	
	def begin(self):
		# Duty cycle for each color, 0-100
		self.red_duty_cycle = 0
		self.green_duty_cycle = 0
		self.blue_duty_cycle = 0
		
		self.red_pwm.start(self.red_duty_cycle)
		self.green_pwm.start(self.green_duty_cycle)
		self.blue_pwm.start(self.blue_duty_cycle)
