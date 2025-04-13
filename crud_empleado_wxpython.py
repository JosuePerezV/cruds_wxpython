import wx

class Empleado:
    def __init__(self, idempleado, nombres, apellidos, direccion, telefono):
        self.idempleado = idempleado
        self.nombres = nombres
        self.apellidos = apellidos
        self.direccion = direccion
        self.telefono = telefono

class EmpleadoCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(EmpleadoCRUD, self).__init__(parent, title=title, size=(600, 400))

        self.empleados = []

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        labels = ["ID Empleado", "Nombres", "Apellidos", "Dirección", "Teléfono"]
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
        for idx, h in enumerate(labels):
            self.lista.InsertColumn(idx, h, width=100)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(vbox)

        btn_add.Bind(wx.EVT_BUTTON, self.agregar)
        btn_update.Bind(wx.EVT_BUTTON, self.actualizar)
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar)
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
        for c in self.empleados:
            index = self.lista.InsertItem(self.lista.GetItemCount(), c.idempleado)
            self.lista.SetItem(index, 1, c.nombres)
            self.lista.SetItem(index, 2, c.apellidos)
            self.lista.SetItem(index, 3, c.direccion)
            self.lista.SetItem(index, 4, c.telefono)

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            nuevo = Empleado(*valores)
            self.empleados.append(nuevo)
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            valores = self.get_inputs()
            self.empleados[idx] = Empleado(*valores)
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            del self.empleados[idx]
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        e = self.empleados[idx]
        valores = [e.idempleado, e.nombres, e.apellidos, e.direccion, e.telefono]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = EmpleadoCRUD(None, "CRUD Empleado")
    app.MainLoop()
