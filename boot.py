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
import vartu_valdymas
import ekranas
led = Pin(2, Pin.OUT)