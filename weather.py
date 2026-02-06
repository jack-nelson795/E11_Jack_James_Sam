import adafruit_bme680
import time
import board

timecount = 0

#create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

while(timecount<10):
	print("\n")
	
	'''
	print(time.ctime())
	print("Temperature: %0.1f C" % bme680.temperature, end = " ")
	print("Gas: %d ohm" % bme680.gas, end = " ")
	print("Humidity: %0.1f %%" % bme680.relative_humidity, end = " ")
	print("Pressure: %0.3f hPa" % bme680.pressure, end = " ")
	print("Altitude = %0.2f meters" % bme680.altitude, end = " ")
	'''
	
	print(f"{time.ctime()} Tempreature: {round(bme680.temperature,1)}C Gas: {int(bme680.gas)}ohm Humidity: {round(bme680.relative_humidity,1)}% Pressure: {round(bme680.pressure,3)}hPa Altitude: {round(bme680.altitude,2)}meters")

	time.sleep(2)
	timecount += 2
