import wx

class Membresia:
    def __init__(self, id_tarjeta, puntos, fecha_emision, fecha_expiracion):
        self.id_tarjeta = id_tarjeta
        self.puntos = puntos
        self.fecha_emision = fecha_emision
        self.fecha_expiracion = fecha_expiracion

class MembresiaCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(MembresiaCRUD, self).__init__(parent, title=title, size=(600, 400))

        self.membresias = []

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        labels = ["ID Tarjeta", "Puntos Acumulados", "Fecha Emisión", "Fecha Expiración"]
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
            self.lista.InsertColumn(idx, h, width=140)
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
        for m in self.membresias:
            index = self.lista.InsertItem(self.lista.GetItemCount(), m.id_tarjeta)
            self.lista.SetItem(index, 1, m.puntos)
            self.lista.SetItem(index, 2, m.fecha_emision)
            self.lista.SetItem(index, 3, m.fecha_expiracion)

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            nuevo = Membresia(*valores)
            self.membresias.append(nuevo)
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            valores = self.get_inputs()
            self.membresias[idx] = Membresia(*valores)
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            del self.membresias[idx]
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        m = self.membresias[idx]
        valores = [m.id_tarjeta, m.puntos, m.fecha_emision, m.fecha_expiracion]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MembresiaCRUD(None, "CRUD Membresía")
    app.MainLoop()
