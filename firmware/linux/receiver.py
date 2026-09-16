from arduino.app_utils import App, Bridge
import time


def receive_telemetry(message):
	print("Telemetry received:", message)


Bridge.provide("telemetry", receive_telemetry)


def loop():
	print("Linux telemetry receiver running...")
	time.sleep(2)


App.run(user_loop=loop)
