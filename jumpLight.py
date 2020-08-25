# Import libraries
import time
import datetime
import board
import busio
import adafruit_msa301
import ledshim

# Connect to the accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
msa = adafruit_msa301.MSA301(i2c)

# Initial settings for the LEDs
ledshim.set_clear_on_exit()
ledshim.set_brightness(0.6)

# Important constants
gravity = 9.81 # acceleration due to gravity
accThresh = 40 # some threshold to detect freefall

# Initialize your personal record
jumpPR = 0;

# Find the total acceleration
def netAccFun(i2cName):
	# read from the accelerometer
	x, y, z = msa.acceleration

	# Sum of squares in three directions to find total
	netAcc = x**2 + y**2 + z**2
	return netAcc

# Use the current jump height and your personal record to switch on the lights
def lightShow(jumpVal, jumpPR):
	heightVal = 10*jumpVal*ledshim.NUM_PIXELS
	prVal  =  10*jumpPR*ledshim.NUM_PIXELS

	# Green lights show your current PR
	r, g, b = 0, 255, 0

	if heightVal < prVal:
	# Additional red lights if you don't beat your PR
		r = 255
	else:
	# Additional blue lights if you beat the PR
		b = 255

	# Set LED colors
	for x in range(ledshim.NUM_PIXELS):
		if heightVal < 0:
			r, b = 0, 0
		if prVal < 0:
			g = 0

		ledshim.set_pixel(x, r, g, b)
		heightVal -= 1
		prVal -=1

	# Turn on the LEDs
	ledshim.show()


while True:
	# Check if freefall has started
	if netAccFun(msa) < accThresh:
		print("jump start \n")

		# Record the time
		jumpStart = datetime.datetime.now()

		# Keep running till freefall stops
		while netAccFun(msa) < accThresh:
			time.sleep(0.01)

		print("jump end \n")

		# Record the time
		jumpEnd = datetime.datetime.now()

		# Measure jump duration in seconds
		jumpDuration = (jumpEnd - jumpStart).total_seconds()

		# Use distance equation to measure jump height
		jumpHeight = 0.5*gravity*((0.5*jumpDuration)**2)

		# Turn on the lights
		lightShow(jumpHeight, jumpPR)
		print("%f %f " % (jumpHeight, jumpPR))

		# Reset your personal record
		jumpPR = max(jumpHeight, jumpPR)

		# Wait a bit before the next cycle
		time.sleep(0.5)
