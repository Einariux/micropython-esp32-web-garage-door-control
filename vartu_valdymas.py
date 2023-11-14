import socket
import gc
import ujson
import machine
import time

# GPIO pinai
GPIO_0 = machine.Pin(0, machine.Pin.IN)
GPIO_2 = machine.Pin(2, machine.Pin.OUT)

garage_door_state = "Uzdaryta"  # busena vartu
garage_door_icon = "fas fa-door-closed"  # ikona

# Sukuriame garozo vartus
class GarageDoor:
    def __init__(self):
        self.state = "Uzdaryta"

    def toggle(self):
        if self.state == "Uzdaryta":
            self.state = "Atidaryta"
        else:
            self.state = "Uzdaryta"

garage_door = GarageDoor()

def check_gpio0():
    global garage_door_icon, garage_door_state
    gpio_0_state = GPIO_0.value()
    if gpio_0_state == 0:
        garage_door_icon = "fas fa-door-open"
        garage_door_state = "Atidaryta"
    else:
        garage_door_icon = "fas fa-door-closed"
        garage_door_state = "Uzdaryta"

# Inicializuojame laikmati
last_gpio0_check_time = 0

def web_page():
    global garage_door_icon
    if garage_door_state == "Uzdaryta":
        garage_door_icon = 'fas fa-door-closed" style="color:#0000FF;"'
    else:
        garage_door_icon = 'fas fa-door-open" style="color:#FF0000;"'

    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }

        .door-icon {
            font-size: 3em;
            """ + garage_door_icon + """  /* Nustatome ikonos spalvą ir dydį pagal būseną */
        }
    </style>
</head>

<body>
    <h2>Garazo Vartu Valdymas</h2>
    <p>
        <a href=\"?garage_toggle\"><button class="button">Garazo vartai</button></a>
    </p>
    <p class="door-icon">
        <i class=\"""" + garage_door_icon + """\"></i>  <!-- Pakeista ikona -->
    </p>
    <p>Garazo vartu busena: <strong>""" + garage_door_state + """</strong></p>
</body>

</html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Request Content = %s' % request)
        garage_toggle = request.find('/garage_toggle')
        
        if garage_toggle == 6:
            garage_door.toggle()
            if garage_door.state == "Uzdaryta":
                garage_door_icon = "fas fa-door-closed"
            else:
                garage_door_icon = "fas fa-door-open"
            garage_door_state = garage_door.state
            # Įjungiame GPIO 2
            GPIO_2.on()
            time.sleep(2)  # Palaukiame 2 sekundes
            # Išjungiame GPIO 2
            GPIO_2.off()   

        # Papildyta logika valdyti GPIO per GET ir SET komandas
        elif request.find('/gpio2_on') != -1:
            GPIO_2.value(1)  # Įjungti GPIO 2
        elif request.find('/gpio2_off') != -1:
            GPIO_2.value(0)  # Išjungti GPIO 2

        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_gpio0_check_time) >= 5000:
            check_gpio0()
            last_gpio0_check_time = current_time

        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')
