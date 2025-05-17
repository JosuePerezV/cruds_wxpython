import wx
from conexion import conectar

class ProductoCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(ProductoCRUD, self).__init__(parent, title=title, size=(800, 500))

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
        cursor.execute("SELECT * FROM producto")
        for p in cursor.fetchall():
            index = self.lista.InsertItem(self.lista.GetItemCount(), p[0])
            for i in range(1, len(p)):
                self.lista.SetItem(index, i, str(p[i]))
        conn.close()

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO producto VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", valores)
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
            cursor.execute("""UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, stock=%s,
                              caducidad=%s, categoria=%s, inventario=%s WHERE codigo=%s""",
                           (*valores[1:], valores[0]))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            codigo = self.lista.GetItemText(idx)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producto WHERE codigo=%s", (codigo,))
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
    frame = ProductoCRUD(None, "CRUD Producto")
    app.MainLoop()
