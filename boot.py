# This file is executed on every boot (including wake-boot from deepsleep)
from machine import Pin, I2C, RTC
from vartu_wifi_nustatymai import VartuWIFI
import utime
import esp
esp.osdebug(None)
vw = VartuWIFI()
vw.connect()
import vartu_valdymas
led = Pin(2, Pin.OUT)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)