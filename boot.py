# This file is executed on every boot (including wake-boot from deepsleep)
from machine import Pin
from vartu_wifi_nustatymai import VartuWIFI
import utime
import esp
esp.osdebug(None)
vw = VartuWIFI()
vw.connect()
import vartu_valdymas
led = Pin(2, Pin.OUT)