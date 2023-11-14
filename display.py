import ssd1306
from machine import Pin, I2C, RTC

# Inicializuojame I2C ir SSD1306 ekranėlį
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Inicializuojame WiFi
#sta_if = network.WLAN(network.STA_IF)
#sta_if.active(True)

# Pasiruošiame funkciją gauti IP adresą
def get_ip_address():
    if sta_if.isconnected():
        return sta_if.ifconfig()[0]
    else:
        return "Not connected"

# Pradinis ekranėlio tekstas
display.text("IP Adresas:", 0, 0)
display.show()

# Laikrodis, kuris tikrina ar gautas IP
clock = machine.RTC()

# Pagrindinė programos eiga
while True:
    # Atnaujiname laiką iš NTP
    ntptime.settime()

    # Gauti IP adresą
    ip_address = get_ip_address()

    # Atnaujinti ekraną su IP adresu
    display.fill(0)  # Išvalome ekraną
    display.text("IP Adresas:", 0, 0)
    display.text(ip_address, 0, 20)
    display.show()

    # Palaukime 10 sekundžių prieš atnaujinant
    machine.idle()
    machine.delay(10000)
