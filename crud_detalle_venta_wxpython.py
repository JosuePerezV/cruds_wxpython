import wx
from conexion import conectar

class DetalleVentaCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(DetalleVentaCRUD, self).__init__(parent, title=title, size=(650, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        labels = ["ID Detalle Venta", "ID Venta", "Cantidad", "Código Producto"]
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
            self.lista.InsertColumn(idx, h, width=130)
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
        cursor.execute("SELECT * FROM detalle_venta")
        for d in cursor.fetchall():
            index = self.lista.InsertItem(self.lista.GetItemCount(), str(d[0]))
            self.lista.SetItem(index, 1, str(d[1]))
            self.lista.SetItem(index, 2, str(d[2]))
            self.lista.SetItem(index, 3, str(d[3]))
        conn.close()

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO detalle_venta VALUES (%s, %s, %s, %s)", valores)
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
            cursor.execute("""UPDATE detalle_venta SET id_venta=%s, cantidad=%s, producto_codigo=%s WHERE id_detalle=%s""",
                           (valores[1], valores[2], valores[3], valores[0]))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            id_detalle = self.lista.GetItemText(idx)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM detalle_venta WHERE id_detalle=%s", (id_detalle,))
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
    frame = DetalleVentaCRUD(None, "CRUD Detalle Venta")
    app.MainLoop()
