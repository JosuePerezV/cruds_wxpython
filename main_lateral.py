import wx
from venta_pos import VentaPOS
from crud_cliente_wxpython import ClienteCRUD
from crud_empleado_wxpython import EmpleadoCRUD
from crud_proveedor_wxpython import ProveedorCRUD
from crud_categoria_wxpython import CategoriaCRUD
from crud_membresia_wxpython import MembresiaCRUD
from crud_producto_wxpython import ProductoPanel
from crud_detalle_venta_wxpython import DetalleVentaCRUD
from crud_usuarios_wxpython import UsuarioCRUD

class MenuLateralPOS(wx.Frame):
    def __init__(self, id_empleado):
        super().__init__(None, title="Sistema POS HEB", size=(1200, 750))
        self.id_empleado = id_empleado
        self.SetMinSize(wx.Size(1000, 600))
        self.panel = wx.Panel(self)

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Panel del menú lateral
        menu_panel = wx.Panel(self.panel, size=(200, -1))
        menu_panel.SetBackgroundColour(wx.Colour(50, 50, 50))
        menu_sizer = wx.BoxSizer(wx.VERTICAL)

        # Logo y título
        logo_panel = wx.Panel(menu_panel)
        logo_panel.SetBackgroundColour(wx.Colour(70, 70, 70))
        logo_sizer = wx.BoxSizer(wx.VERTICAL)
        
        titulo = wx.StaticText(logo_panel, label="POS HEB")
        titulo.SetForegroundColour(wx.WHITE)
        font = titulo.GetFont()
        font.PointSize += 6
        font = font.Bold()
        titulo.SetFont(font)
        logo_sizer.Add(titulo, flag=wx.ALL|wx.ALIGN_CENTER, border=15)
        
        logo_panel.SetSizer(logo_sizer)
        menu_sizer.Add(logo_panel, flag=wx.EXPAND)

        # Botones del menú
        botones = [
            ("Punto de Venta", self.abrir_venta, wx.Colour(0, 150, 136)),
            ("Clientes", self.abrir_clientes, wx.Colour(0, 114, 198)),
            ("Empleados", self.abrir_empleados, wx.Colour(255, 152, 0)),
            ("Proveedores", self.abrir_proveedores, wx.Colour(156, 39, 176)),
            ("Categorías", self.abrir_categorias, wx.Colour(121, 85, 72)),
            ("Membresías", self.abrir_membresias, wx.Colour(0, 77, 64)),
            ("Productos", self.abrir_productos, wx.Colour(216, 27, 96)),
            ("Ventas", self.abrir_detalle_venta, wx.Colour(27, 94, 32)),
            ("Usuarios", self.abrir_usuarios, wx.Colour(74, 20, 140))
        ]

        for texto, funcion, color in botones:
            btn = wx.Button(menu_panel, label=texto, size=(180, 45))
            btn.SetBackgroundColour(color)
            btn.SetForegroundColour(wx.WHITE)
            btn.Bind(wx.EVT_BUTTON, funcion)
            menu_sizer.Add(btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)

        # Botón de salir
        btn_salir = wx.Button(menu_panel, label="Salir", size=(180, 45))
        btn_salir.SetBackgroundColour(wx.Colour(198, 40, 40))
        btn_salir.SetForegroundColour(wx.WHITE)
        btn_salir.Bind(wx.EVT_BUTTON, lambda e: self.Close())
        menu_sizer.Add(btn_salir, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=5)

        menu_panel.SetSizer(menu_sizer)
        main_sizer.Add(menu_panel, 0, wx.EXPAND)

        # Área de contenido
        self.area_contenido = wx.Panel(self.panel)
        self.area_contenido.SetBackgroundColour(wx.WHITE)
        self.content_sizer = wx.BoxSizer(wx.VERTICAL)
        self.area_contenido.SetSizer(self.content_sizer)
        
        # Mostrar el módulo de ventas por defecto
        self.abrir_venta(None)
        
        main_sizer.Add(self.area_contenido, 1, wx.EXPAND|wx.ALL, 5)

        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.Show()

    def limpiar_contenido(self):
        for child in self.area_contenido.GetChildren():
            child.Destroy()
        self.area_contenido.Layout()

    def abrir_venta(self, event):
        self.limpiar_contenido()
        panel = VentaPOS(self.area_contenido, id_empleado=self.id_empleado)
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Punto de Venta")

    def abrir_clientes(self, event):
        self.limpiar_contenido()
        panel = ClienteCRUD(self.area_contenido, "Gestión de Clientes")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Clientes")

    def abrir_empleados(self, event):
        self.limpiar_contenido()
        panel = EmpleadoCRUD(self.area_contenido, "Gestión de Empleados")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Empleados")

    def abrir_proveedores(self, event):
        self.limpiar_contenido()
        panel = ProveedorCRUD(self.area_contenido, "Gestión de Proveedores")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Proveedores")

    def abrir_categorias(self, event):
        self.limpiar_contenido()
        panel = CategoriaCRUD(self.area_contenido, "Gestión de Categorías")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Categorías")

    def abrir_membresias(self, event):
        self.limpiar_contenido()
        panel = MembresiaCRUD(self.area_contenido, "Gestión de Membresías")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Membresías")

    def abrir_productos(self, event):
        self.limpiar_contenido()
        panel = ProductoPanel(self.area_contenido)
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Productos")

    def abrir_detalle_venta(self, event):
        self.limpiar_contenido()
        panel = DetalleVentaCRUD(self.area_contenido, "Gestión de Ventas")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Ventas")

    def abrir_usuarios(self, event):
        self.limpiar_contenido()
        panel = UsuarioCRUD(self.area_contenido, "Gestión de Usuarios")
        self.content_sizer.Add(panel, 1, wx.EXPAND)
        self.area_contenido.Layout()
        self.SetTitle("Sistema POS HEB - Usuarios")

if __name__ == '__main__':
    app = wx.App(False)
    frame = MenuLateralPOS(id_empleado=1)  # para pruebas directas sin login
    app.MainLoop()
