import wx

class Categoria:
    def __init__(self, id_categoria, nombre, descripcion):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

class CategoriaCRUD(wx.Frame):
    def __init__(self, parent, title):
        super(CategoriaCRUD, self).__init__(parent, title=title, size=(600, 400))

        self.categorias = []

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label="ID Categoría:"), flag=wx.RIGHT, border=8)
        self.txt_id = wx.TextCtrl(panel)
        hbox1.Add(self.txt_id, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.RIGHT, border=33)
        self.txt_nombre = wx.TextCtrl(panel)
        hbox2.Add(self.txt_nombre, proportion=1)
        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(panel, label="Descripción:"), flag=wx.RIGHT, border=10)
        self.txt_desc = wx.TextCtrl(panel)
        hbox3.Add(self.txt_desc, proportion=1)
        vbox.Add(hbox3, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_add = wx.Button(panel, label="Agregar")
        self.btn_update = wx.Button(panel, label="Actualizar")
        self.btn_delete = wx.Button(panel, label="Eliminar")
        hbox4.Add(self.btn_add)
        hbox4.Add(self.btn_update, flag=wx.LEFT, border=5)
        hbox4.Add(self.btn_delete, flag=wx.LEFT, border=5)
        vbox.Add(hbox4, flag=wx.ALIGN_CENTER|wx.TOP, border=10)

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

    def agregar_categoria(self, event):
        id_cat = self.txt_id.GetValue()
        nombre = self.txt_nombre.GetValue()
        descripcion = self.txt_desc.GetValue()
        
        if id_cat and nombre:
            cat = Categoria(id_cat, nombre, descripcion)
            self.categorias.append(cat)
            self.actualizar_lista()
            self.limpiar_campos()

    def actualizar_categoria(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion >= 0:
            self.categorias[seleccion].id_categoria = self.txt_id.GetValue()
            self.categorias[seleccion].nombre = self.txt_nombre.GetValue()
            self.categorias[seleccion].descripcion = self.txt_desc.GetValue()
            self.actualizar_lista()
            self.limpiar_campos()

    def eliminar_categoria(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion >= 0:
            del self.categorias[seleccion]
            self.actualizar_lista()
            self.limpiar_campos()

    def seleccionar_item(self, event):
        seleccion = event.GetIndex()
        cat = self.categorias[seleccion]
        self.txt_id.SetValue(cat.id_categoria)
        self.txt_nombre.SetValue(cat.nombre)
        self.txt_desc.SetValue(cat.descripcion)

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        for cat in self.categorias:
            index = self.lista.InsertItem(self.lista.GetItemCount(), cat.id_categoria)
            self.lista.SetItem(index, 1, cat.nombre)
            self.lista.SetItem(index, 2, cat.descripcion)

    def limpiar_campos(self):
        self.txt_id.SetValue("")
        self.txt_nombre.SetValue("")
        self.txt_desc.SetValue("")

if __name__ == '__main__':
    app = wx.App(False)
    frame = CategoriaCRUD(None, "CRUD Categoría")
    app.MainLoop()
