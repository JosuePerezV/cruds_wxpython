import wx

class Producto:
    def __init__(self, codigo, nombre, descripcion, precio, stock, caducidad, categoria, inventario):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.caducidad = caducidad
        self.categoria = categoria
        self.inventario = inventario

class ProductoCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(ProductoCRUD, self).__init__(parent, title=title, size=(800, 500))

        self.productos = []

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        labels = ["Código", "Nombre", "Descripción", "Precio", "Stock", "Caducidad", "Categoría", "Inventario"]
        self.inputs = []

        for label in labels:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(panel, label=label+":"), flag=wx.RIGHT, border=8)
            txt = wx.TextCtrl(panel)
            self.inputs.append(txt)
            hbox.Add(txt, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        btn_add = wx.Button(panel, label="Agregar")
        btn_update = wx.Button(panel, label="Actualizar")
        btn_delete = wx.Button(panel, label="Eliminar")
        hbox_buttons.Add(btn_add)
        hbox_buttons.Add(btn_update, flag=wx.LEFT, border=5)
        hbox_buttons.Add(btn_delete, flag=wx.LEFT, border=5)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

        self.lista = wx.ListCtrl(panel, style=wx.LC_REPORT)
        headers = ["Código", "Nombre", "Descripción", "Precio", "Stock", "Caducidad", "Categoría", "Inventario"]
        for idx, h in enumerate(headers):
            self.lista.InsertColumn(idx, h, width=100)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(vbox)

        btn_add.Bind(wx.EVT_BUTTON, self.agregar_producto)
        btn_update.Bind(wx.EVT_BUTTON, self.actualizar_producto)
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_producto)
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)

        self.Centre()
        self.Show()

    def get_inputs(self):
        return [i.GetValue() for i in self.inputs]

    def set_inputs(self, values):
        for i, val in zip(self.inputs, values):
            i.SetValue(val)

    def limpiar_campos(self):
        for i in self.inputs:
            i.SetValue("")

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        for p in self.productos:
            index = self.lista.InsertItem(self.lista.GetItemCount(), p.codigo)
            self.lista.SetItem(index, 1, p.nombre)
            self.lista.SetItem(index, 2, p.descripcion)
            self.lista.SetItem(index, 3, str(p.precio))
            self.lista.SetItem(index, 4, str(p.stock))
            self.lista.SetItem(index, 5, p.caducidad)
            self.lista.SetItem(index, 6, p.categoria)
            self.lista.SetItem(index, 7, p.inventario)

    def agregar_producto(self, event):
        valores = self.get_inputs()
        if all(valores):
            nuevo = Producto(*valores)
            self.productos.append(nuevo)
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar_producto(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            valores = self.get_inputs()
            self.productos[idx] = Producto(*valores)
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar_producto(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            del self.productos[idx]
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        prod = self.productos[idx]
        valores = [prod.codigo, prod.nombre, prod.descripcion, str(prod.precio), str(prod.stock), prod.caducidad, prod.categoria, prod.inventario]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = ProductoCRUD(None, "CRUD Producto")
    app.MainLoop()
