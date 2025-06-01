import wx
import os
from conexion import conectar
from main_lateral import MenuLateralPOS

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Login - Sistema POS HEB", size=(400, 500))
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Logo de HEB
        logo_path = os.path.join("assets", "logo_heb.png")
        if os.path.exists(logo_path):
            img = wx.Image(logo_path, wx.BITMAP_TYPE_PNG).Scale(320, 120)
            logo_bitmap = wx.StaticBitmap(panel, bitmap=wx.Bitmap(img))
            vbox.Add(logo_bitmap, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=20)

        # Título
        titulo = wx.StaticText(panel, label="Inicio de Sesión")
        font = titulo.GetFont()
        font.PointSize += 4
        font = font.Bold()
        titulo.SetFont(font)
        vbox.Add(titulo, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=15)

        # Formulario de usuario y contraseña
        grid = wx.FlexGridSizer(2, 2, 10, 10)
        grid.Add(wx.StaticText(panel, label="Usuario:"))
        self.txt_usuario = wx.TextCtrl(panel)
        grid.Add(self.txt_usuario)

        grid.Add(wx.StaticText(panel, label="Contraseña:"))
        self.txt_contrasena = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        grid.Add(self.txt_contrasena)

        vbox.Add(grid, flag=wx.ALL | wx.ALIGN_CENTER, border=20)

        # Botón de ingreso
        btn_login = wx.Button(panel, label="Ingresar", size=(120, 35))
        btn_login.Bind(wx.EVT_BUTTON, self.verificar_credenciales)
        vbox.Add(btn_login, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def verificar_credenciales(self, event):
        usuario = self.txt_usuario.GetValue().strip()
        contrasena = self.txt_contrasena.GetValue().strip()

        if not usuario or not contrasena:
            wx.MessageBox("Por favor, ingresa usuario y contraseña", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.usuario, u.cargo, CONCAT(e.nombres, ' ', e.apellidos), e.idempleado
                FROM usuarios u
                JOIN empleado e ON u.id_empleado = e.idempleado
                WHERE u.usuario = %s AND u.contrasena = %s
            """, (usuario, contrasena))
            resultado = cursor.fetchone()
            conn.close()

            if resultado:
                nombre_empleado = resultado[2]
                id_empleado = resultado[3]
                wx.MessageBox(f"Bienvenido, {nombre_empleado}", "Éxito", wx.OK | wx.ICON_INFORMATION)
                self.Hide()
                MenuLateralPOS(id_empleado=id_empleado).Show()
            else:
                wx.MessageBox("Credenciales incorrectas", "Acceso denegado", wx.OK | wx.ICON_ERROR)

        except Exception as err:
            wx.MessageBox(f"Error al conectar con la base de datos: {err}", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = LoginFrame()
    app.MainLoop()
