from obswebsocket import obsws, requests
import json
import keyboard
import time
import os
# Genera QR con ip Privada
import socket
import qrcode
import qrcode.constants
import qrcode.image.svg

# Consigue ip privada

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    c.connect(("8.8.8.8", 8080))
    ip_priv = c.getsockname()[0]
finally:
    c.close()
print(ip_priv)
url = f'http://{ip_priv}:80/'

# Genera QR

q = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    image_factory=qrcode.image.svg.SvgPathImage
)
q.add_data(url)
q.make(fit=True)

img_qr = q.make_image(attrib={'class': 'some-css-class'})
img = img_qr.to_string(encoding='unicode') # SVG en texto plano
# Guarda el QR
print(img)

keylist = {}
num = 0


while True:
    try:
        key  = str(keyboard.read_key())
        print(key)
        if not key in keylist.values():
            keylist[num] = key
            num += 1
            print(f'Agregada: {key}')
    except KeyboardInterrupt:
        print(keylist)
        with open('Media.json', 'w') as a:
            json.dump(keylist, a)
        exit()

client = obsws(host='localhost', port=4455, password='123456')
client.connect()

data = client.call(requests.GetVersion())
myJson = {
    'name': data.name,
    'availableRequests': data.datain['availableRequests'],
    'obsVersion': data.datain['obsVersion'],
    'obsWebSocketVersion': data.datain['obsWebSocketVersion'],
    'platform': data.datain['platform'],
    'platformDescription': data.datain['platformDescription'],
    'rpcVersion': data.datain['rpcVersion'],
    'supportedImageFormats': data.datain['supportedImageFormats']
}
print(f"{myJson} \n\n ")
# print(f'Data de GetVersion | Requests: {vars(data)}')
print(f"Nombre de Llamada: {data.name}")
print(f"Requests Validas: {data.datain['availableRequests']}")
print(f"Version de OBS: {data.datain['obsVersion']}")
print(f"Version de OBS Web Socket: {data.datain['obsWebSocketVersion']}")
print(f"Plataforma: {data.datain['platform']}")
print(f"Descripcion de plataforma: {data.datain['platformDescription']}")
print(f"Version de RPC: {data.datain['rpcVersion']}")
print(f"Formatos soportado de imagenes: {data.datain['supportedImageFormats']}")

dataStats = client.call(requests.GetStats())
# print(f'Data de GetStats | Requests: {vars(dataStats)}')
print(f"Nombre de Llamada: {dataStats.name}")
print(f"FPS actuales renderizados: {dataStats.datain['activeFps']}")
print(f"Espacio disponible: {dataStats.datain['availableDiskSpace']}")
print(f"Tiempo Promedio de renderizado de OBS por FPS: {dataStats.datain['averageFrameRenderTime']}")
print(f"CPU usado actualmente | porcentaje: {dataStats.datain['cpuUsage']}")
print(f"Memoria usada en MB por OBS: {dataStats.datain['memoryUsage']}")
print(f"Fotogramas omitidos por OBS en salida de hilos: {dataStats.datain['outputSkippedFrames']}")
print(f"Total de FPS generados por hilo de salida: {dataStats.datain['outputTotalFrames']}")
print(f"FPS omitidos por OBS en hilo de renderizado: {dataStats.datain['renderSkippedFrames']}")
print(f"FPS Generados por hilo de renderizado: {dataStats.datain['renderTotalFrames']}")
print(f"Mensajes recibidos por el obs-websocket del cliente: {dataStats.datain['webSocketSessionIncomingMessages']}")
print(f"Mensajes enviados por obs-websocket al cliente: {dataStats.datain['webSocketSessionOutgoingMessages']}")
print(f"Datos de salida: {dataStats.dataout}")
print(f"Estado: {dataStats.status}")

dataHotkey = client.call(requests.GetHotKeyList())
# print(f"Data de GetHotkeyList: {vars(dataHotkey)}")
print(f"Nombre de Llamada: {dataHotkey.name}")
print(f"Datos de entrada: {dataHotkey.datain}")
print(f"Datos de salida: {dataHotkey.dataout}")
print(f"Estado: {dataHotkey.status}")

dataScennes = client.call(requests.GetSceneList())
print(f"Datos de GetSceneList | Requests: {vars(dataScennes)}")
print(f"Nombre de Llamada: {dataScennes.name}")
print(f"Escena actual: {dataScennes.datain['currentPreviewSceneName']}")
print(f"UID de Esecna actual: {dataScennes.datain['currentPreviewSceneUuid']}")
print(f"Lista de escenas: {dataScennes.datain['scenes']}")


































# import keyboard

# while True:
#     try:
#         key = keyboard.read_key()
#         print(key)
#     except Exception as e:
#         print('Programa finalizado')