# This file is executed on every boot (including wake-boot from deepsleep)
from machine import Pin, I2C, RTC
from vartu_wifi_nustatymai import VartuWIFI
import machine
import utime
import esp
import upip
import ntptime
esp.osdebug(None)
vw = VartuWIFI()
vw.connect()
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
import vartu_valdymas
import ekranas
led = Pin(2, Pin.OUT)
