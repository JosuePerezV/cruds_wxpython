import wx
from conexion import conectar

class CategoriaCRUD(wx.Panel):
    def __init__(self, parent, title):
        super(CategoriaCRUD, self).__init__(parent)
        
        self.SetBackgroundColour(wx.WHITE)
        
        # Sizer principal
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Título
        titulo = wx.StaticText(self, label=title)
        titulo.SetForegroundColour(wx.Colour(0, 64, 128))
        font = titulo.GetFont()
        font.PointSize += 6
        font = font.Bold()
        titulo.SetFont(font)
        vbox.Add(titulo, flag=wx.ALL|wx.ALIGN_CENTER, border=10)
        
        # Panel de formulario
        form_panel = wx.Panel(self)
        form_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        form_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Campos de entrada
        self.txt_id = wx.TextCtrl(form_panel)
        self.txt_nombre = wx.TextCtrl(form_panel)
        self.txt_desc = wx.TextCtrl(form_panel, style=wx.TE_MULTILINE, size=(-1, 60))
        
        campos = [
            ("ID Categoría:", self.txt_id),
            ("Nombre:", self.txt_nombre),
            ("Descripción:", self.txt_desc)
        ]
        
        for label, ctrl in campos:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((120, -1))
            hbox.Add(lbl, flag=wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=8)
            hbox.Add(ctrl, proportion=1, flag=wx.EXPAND)
            form_sizer.Add(hbox, flag=wx.EXPAND|wx.ALL, border=5)
        
        # Botones
        btn_panel = wx.Panel(form_panel)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_add = wx.Button(btn_panel, label="Agregar", size=(100, 30))
        self.btn_update = wx.Button(btn_panel, label="Actualizar", size=(100, 30))
        self.btn_delete = wx.Button(btn_panel, label="Eliminar", size=(100, 30))
        
        self.btn_add.SetBackgroundColour(wx.Colour(0, 128, 0))
        self.btn_add.SetForegroundColour(wx.WHITE)
        self.btn_update.SetBackgroundColour(wx.Colour(0, 0, 128))
        self.btn_update.SetForegroundColour(wx.WHITE)
        self.btn_delete.SetBackgroundColour(wx.Colour(128, 0, 0))
        self.btn_delete.SetForegroundColour(wx.WHITE)
        
        btn_sizer.Add(self.btn_add, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_update, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_delete)
        btn_panel.SetSizer(btn_sizer)
        form_sizer.Add(btn_panel, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        
        form_panel.SetSizer(form_sizer)
        vbox.Add(form_panel, flag=wx.EXPAND|wx.ALL, border=5)
        
        # Lista de categorías
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.lista.SetMinSize((-1, 200))
        self.lista.InsertColumn(0, 'ID', width=70)
        self.lista.InsertColumn(1, 'Nombre', width=180)
        self.lista.InsertColumn(2, 'Descripción', width=300)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.SetSizer(vbox)
        
        # Eventos
        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar_categoria)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar_categoria)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_categoria)
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)
        
        self.actualizar_lista()

    def agregar_categoria(self, event):
        id_cat = self.txt_id.GetValue().strip()
        nombre = self.txt_nombre.GetValue().strip()
        descripcion = self.txt_desc.GetValue().strip()
        
        if not id_cat:
            wx.MessageBox("El ID de categoría es obligatorio", "Error", wx.OK|wx.ICON_ERROR)
            self.txt_id.SetFocus()
            return
            
        if not nombre:
            wx.MessageBox("El nombre de categoría es obligatorio", "Error", wx.OK|wx.ICON_ERROR)
            self.txt_nombre.SetFocus()
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO categoria (id_categoria, nombre, descripcion) VALUES (%s, %s, %s)",
                (id_cat, nombre, descripcion)
            )
            conn.commit()
            wx.MessageBox("Categoría agregada correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al agregar categoría: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def actualizar_categoria(self, event):
        id_cat = self.txt_id.GetValue().strip()
        nombre = self.txt_nombre.GetValue().strip()
        descripcion = self.txt_desc.GetValue().strip()
        
        if not id_cat:
            wx.MessageBox("Seleccione una categoría para actualizar", "Error", wx.OK|wx.ICON_ERROR)
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE categoria SET nombre=%s, descripcion=%s WHERE id_categoria=%s",
                (nombre, descripcion, id_cat))
            conn.commit()
            wx.MessageBox("Categoría actualizada correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar categoría: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def eliminar_categoria(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion < 0:
            wx.MessageBox("Seleccione una categoría para eliminar", "Error", wx.OK|wx.ICON_ERROR)
            return
            
        id_cat = self.lista.GetItemText(seleccion)
        
        confirm = wx.MessageBox(
            f"¿Está seguro que desea eliminar la categoría {id_cat}?",
            "Confirmar eliminación", 
            wx.YES_NO|wx.ICON_QUESTION
        )
        
        if confirm != wx.YES:
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categoria WHERE id_categoria=%s", (id_cat,))
            conn.commit()
            wx.MessageBox("Categoría eliminada correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar categoría: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def seleccionar_item(self, event):
        seleccion = event.GetIndex()
        self.txt_id.SetValue(self.lista.GetItemText(seleccion))
        self.txt_nombre.SetValue(self.lista.GetItem(seleccion, 1).GetText())
        self.txt_desc.SetValue(self.lista.GetItem(seleccion, 2).GetText())

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM categoria ORDER BY nombre")
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                self.lista.SetItem(index, 1, row[1])
                self.lista.SetItem(index, 2, row[2] if row[2] else "")
        except Exception as e:
            wx.MessageBox(f"Error al cargar categorías: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def limpiar_campos(self):
        self.txt_id.SetValue("")
        self.txt_nombre.SetValue("")
        self.txt_desc.SetValue("")