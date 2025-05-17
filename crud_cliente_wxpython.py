import wx
from conexion import conectar

class ClienteCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(ClienteCRUD, self).__init__(parent, title=title, size=(600, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        labels = ["ID Cliente", "Nombres", "Apellidos", "Teléfono", "Email"]
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
        self.actualizar_lista()

    def get_inputs(self):
        return [i.GetValue() for i in self.inputs]

    def set_inputs(self, values):
        for i, val in zip(self.inputs, values):
            i.SetValue(str(val))

    def limpiar_campos(self):
        for i in self.inputs:
            i.SetValue("")

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        for c in cursor.fetchall():
            index = self.lista.InsertItem(self.lista.GetItemCount(), str(c[0]))
            self.lista.SetItem(index, 1, c[1])
            self.lista.SetItem(index, 2, c[2])
            self.lista.SetItem(index, 3, c[3])
            self.lista.SetItem(index, 4, c[4])
        conn.close()

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO cliente VALUES (%s, %s, %s, %s, %s)", valores)
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            valores = self.get_inputs()
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""UPDATE cliente SET nombres=%s, apellidos=%s, telefono=%s, email=%s WHERE idcliente=%s""",
                           (valores[1], valores[2], valores[3], valores[4], valores[0]))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            idcliente = self.lista.GetItemText(idx)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cliente WHERE idcliente=%s", (idcliente,))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        valores = [self.lista.GetItem(idx, i).GetText() for i in range(len(self.inputs))]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = ClienteCRUD(None, "CRUD Cliente")
    app.MainLoop()
