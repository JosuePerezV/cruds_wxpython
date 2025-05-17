import wx
from conexion import conectar

class CategoriaCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(CategoriaCRUD, self).__init__(parent, title=title, size=(600, 400))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.txt_id = wx.TextCtrl(panel)
        self.txt_nombre = wx.TextCtrl(panel)
        self.txt_desc = wx.TextCtrl(panel)

        campos = [("ID Categoría:", self.txt_id), ("Nombre:", self.txt_nombre), ("Descripción:", self.txt_desc)]

        for label, ctrl in campos:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(wx.StaticText(panel, label=label), flag=wx.RIGHT, border=8)
            hbox.Add(ctrl, proportion=1)
            vbox.Add(hbox, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=5)

        hbox_buttons = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_add = wx.Button(panel, label="Agregar")
        self.btn_update = wx.Button(panel, label="Actualizar")
        self.btn_delete = wx.Button(panel, label="Eliminar")
        hbox_buttons.Add(self.btn_add)
        hbox_buttons.Add(self.btn_update, flag=wx.LEFT, border=5)
        hbox_buttons.Add(self.btn_delete, flag=wx.LEFT, border=5)
        vbox.Add(hbox_buttons, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

        self.lista = wx.ListCtrl(panel, style=wx.LC_REPORT)
        self.lista.InsertColumn(0, 'ID', width=70)
        self.lista.InsertColumn(1, 'Nombre', width=140)
        self.lista.InsertColumn(2, 'Descripción', width=250)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar_categoria)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar_categoria)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_categoria)
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)

        self.Centre()
        self.Show()
        self.actualizar_lista()

    def agregar_categoria(self, event):
        id_cat = self.txt_id.GetValue()
        nombre = self.txt_nombre.GetValue()
        descripcion = self.txt_desc.GetValue()
        if id_cat and nombre:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categoria (id_categoria, nombre, descripcion) VALUES (%s, %s, %s)",
                           (id_cat, nombre, descripcion))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar_categoria(self, event):
        id_cat = self.txt_id.GetValue()
        nombre = self.txt_nombre.GetValue()
        descripcion = self.txt_desc.GetValue()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE categoria SET nombre=%s, descripcion=%s WHERE id_categoria=%s",
                       (nombre, descripcion, id_cat))
        conn.commit()
        conn.close()
        self.actualizar_lista()
        self.limpiar_campos()

    def eliminar_categoria(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion >= 0:
            id_cat = self.lista.GetItemText(seleccion)
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categoria WHERE id_categoria=%s", (id_cat,))
            conn.commit()
            conn.close()
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        seleccion = event.GetIndex()
        self.txt_id.SetValue(self.lista.GetItemText(seleccion))
        self.txt_nombre.SetValue(self.lista.GetItem(seleccion, 1).GetText())
        self.txt_desc.SetValue(self.lista.GetItem(seleccion, 2).GetText())

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categoria")
        for row in cursor.fetchall():
            index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
            self.lista.SetItem(index, 1, row[1])
            self.lista.SetItem(index, 2, row[2])
        conn.close()

    def limpiar_campos(self):
        self.txt_id.SetValue("")
        self.txt_nombre.SetValue("")
        self.txt_desc.SetValue("")

if __name__ == '__main__':
    app = wx.App(False)
    frame = CategoriaCRUD(None, "CRUD Categoría")
    app.MainLoop()
