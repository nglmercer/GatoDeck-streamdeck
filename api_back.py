import keyboard
from api_obs import apiObs
import socket
import qrcode
import qrcode.constants
import qrcode.image.svg
import re

class API_BACK:
    def __init__(self) -> None:
        self.actions2 = {
            "132": "start application 1",
            "133": "browser search key",
            "134": "start application 2",
            "135": "select media",
            "135": "play/pause media",
            "140": "volume mute",
            "141": "volume down",
            "142": "volume up",
            "57": "right shift",
            "59": "right ctrl",
            "61": "right alt",
            "62": "alt",
            "63": "ctrl",
            "64": "left windows",
            "65": "caps lock",
            "70": "delete",
            "71": "end",
            "72": "page down",
            "73": "page up",
            "74": "home",
            "75": "insert",
            "76": "print screen",
            "77": "scroll lock",
            "78": "pause",
        }
        self.actions = {
            'copy': 'ctrl+c',
            'page': 'ctrl+v',
            'cute': 'ctrl+x',
            'paper': 'win+v',
            'mute': 'ctrl+shift+pagedown',
            'ensor': 'ctrl+shift+pageup',
            'next': 'next track',
            'previous': 'previous track',
            'play/pause': 'play/pause media',
            'stop': 'stop media',
            'volume-mute': 'volume mute',
            'volume-down': 'volume down',
            'volume-up': 'volume up'
        }
        self.qr_activo = False
        self.qr_svg, self.qr_data = self.get_qr_ip()

    def action_btn(self, action: str):
        '''
        Ejecuta acciones de atajos de teclado.
        '''
 
        if action in self.actions:
            keyboard.press_and_release(self.actions[action])
            return f'Accion realizada: {action}'
        else:
            return 'Accion no realizadd'

    def press(self, action: str):
        '''
        Codigo de Melsern para manejar excepciones de errores.
        '''
        try:
            keyboard.press_and_release(action)
            print(f"Tecla '{action}' existe y se puede presionar y soltar correctamente.")
        except ValueError:
            print(f"Tecla '{action}' no existe o no se puede presionar y soltar.")
            for key, value in self.actions2.items():
                if value.lower() == action.lower():
                    try:
                        keyboard.press_and_release(key)
                        print(f"Se encontró una tecla similar en actions2: '{value}', y se presionó y soltó correctamente.")
                        break
                    except ValueError:
                        print(f"No se pudo simular la tecla '{value}' desde actions2.")
            else:
                print("No se encontró ninguna tecla similar en actions2.")

    def get_ip(self):
        c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            c.connect(("8.8.8.8", 8080))
            ip_priv = c.getsockname()[0]
        finally:
            c.close()
        return ip_priv

    def get_qr_ip(self):
        '''
        Obtiene la ip privada y la devuelve en texto plano para SVG
        '''
        # c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # try:
        #     c.connect(("8.8.8.8", 80))
        #     ip_priv = c.getsockname()[0]
        # finally:
        #     c.close()
        
        url = f'http://{self.get_ip()}:8080/'

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
        # Guardar png
        png = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        png.add_data(url)
        png.make(fit=True)
        png = png.make_image(fill_color="black", back_color="white")
        png.save(f'static/qr.png')
        # Guarda SVG
        img_qr = q.make_image(attrib={'class': 'some-css-class'})
        img = img_qr.to_string(encoding='unicode') # SVG en texto plano
        # Guarda el QR
        self.qr_svg = img
        data = re.search(r'<path d="([^"]*)"', img)
        if data and self.qr_activo == False:
            a = str(data.groups(1))
            a = a.replace("('", "").replace("',)", "")
            print(self.qr_activo)
            self.qr_activo = True
        return img, a

apiBack = API_BACK()
