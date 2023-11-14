import machine
import network

# Priskiriam I2C sasaja ekranui


# Inicializuojame WiFi
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

# Gaunam IP adresa
def get_ip_address():
    if sta_if.isconnected():
        return sta_if.ifconfig()[0]
    else:
        return "Neprisijungta"

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
    ddisplay.text(ip_address, 0, 40)
    display.show()

    # Palaukime 10 sekundžių prieš atnaujinant
    machine.idle()
    machine.delay(10000)
