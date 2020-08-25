import time
import board
import busio
import adafruit_msa301

i2c = busio.I2C(board.SCL, board.SDA)

msa = adafruit_msa301.MSA301(i2c)
msa.enable_tap_detection()

while True:
	x, y, z = msa.acceleration
	netAcc = x**2 + y**2 + z**2
	if netAcc > 300:
		print("%f" % netAcc)
	time.sleep(0.01)

