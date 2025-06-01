import wx
from conexion import conectar

class ProveedorCRUD(wx.Panel):
    def __init__(self, parent, title):
        super(ProveedorCRUD, self).__init__(parent)

        self.SetBackgroundColour(wx.WHITE)

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
        form_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        form_sizer.AddGrowableCol(1)

        # Campos
        labels = ["ID Proveedor:", "Nombre:", "Teléfono:", "Dirección:"]
        self.inputs = []

        for label in labels:
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((120, -1))
            form_sizer.Add(lbl, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5)

            if label == "ID Proveedor:":
                txt = wx.TextCtrl(form_panel)
                txt.SetEditable(False)
            else:
                txt = wx.TextCtrl(form_panel)
            self.inputs.append(txt)
            form_sizer.Add(txt, flag=wx.EXPAND|wx.RIGHT, border=5)

        # Botones
        btn_panel = wx.Panel(form_panel)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_add = wx.Button(btn_panel, label="Agregar", size=(100, 30))
        self.btn_update = wx.Button(btn_panel, label="Actualizar", size=(100, 30))
        self.btn_delete = wx.Button(btn_panel, label="Eliminar", size=(100, 30))
        self.btn_clear = wx.Button(btn_panel, label="Limpiar", size=(100, 30))

        self.btn_add.SetBackgroundColour(wx.Colour(0, 128, 0))
        self.btn_add.SetForegroundColour(wx.WHITE)
        self.btn_update.SetBackgroundColour(wx.Colour(0, 0, 128))
        self.btn_update.SetForegroundColour(wx.WHITE)
        self.btn_delete.SetBackgroundColour(wx.Colour(128, 0, 0))
        self.btn_delete.SetForegroundColour(wx.WHITE)
        self.btn_clear.SetBackgroundColour(wx.Colour(128, 128, 0))
        self.btn_clear.SetForegroundColour(wx.WHITE)

        btn_sizer.Add(self.btn_add, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_update, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_delete, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_clear)

        btn_panel.SetSizer(btn_sizer)
        form_sizer.Add(wx.StaticText(form_panel), flag=wx.EXPAND)
        form_sizer.Add(btn_panel, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        form_panel.SetSizer(form_sizer)
        vbox.Add(form_panel, flag=wx.EXPAND|wx.ALL, border=5)

        # Lista
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        columnas = ["ID", "Nombre", "Teléfono", "Dirección"]
        for i, col in enumerate(columnas):
            self.lista.InsertColumn(i, col, width=120 if i == 0 else 150)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(vbox)

        # Eventos
        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar)
        self.btn_clear.Bind(wx.EVT_BUTTON, lambda e: self.limpiar_campos())
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)

        self.actualizar_lista()

    def get_inputs(self):
        return [ctrl.GetValue().strip() for ctrl in self.inputs]

    def set_inputs(self, values):
        for ctrl, value in zip(self.inputs, values):
            ctrl.SetValue(str(value))

    def limpiar_campos(self):
        for ctrl in self.inputs:
            ctrl.SetValue("")
        self.inputs[0].SetFocus()

    def validar_campos(self, valores):
        if not valores[1]:
            wx.MessageBox("El nombre del proveedor es obligatorio", "Error", wx.OK|wx.ICON_ERROR)
            self.inputs[1].SetFocus()
            return False
        return True

    def agregar(self, event):
        valores = self.get_inputs()
        if not self.validar_campos(valores):
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO proveedor (nombre, telefono, direccion) VALUES (%s, %s, %s)",
                (valores[1], valores[2], valores[3])
            )
            conn.commit()
            wx.MessageBox("Proveedor agregado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al agregar proveedor: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def actualizar(self, event):
        valores = self.get_inputs()
        if not valores[0]:
            wx.MessageBox("Seleccione un proveedor para actualizar", "Error", wx.OK|wx.ICON_ERROR)
            return
        if not self.validar_campos(valores):
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE proveedor SET nombre=%s, telefono=%s, direccion=%s WHERE idproveedor=%s",
                (valores[1], valores[2], valores[3], valores[0])
            )
            conn.commit()
            wx.MessageBox("Proveedor actualizado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar proveedor: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx < 0:
            wx.MessageBox("Seleccione un proveedor para eliminar", "Error", wx.OK|wx.ICON_ERROR)
            return
        id_proveedor = self.lista.GetItemText(idx)
        confirm = wx.MessageBox(
            f"¿Está seguro que desea eliminar al proveedor {id_proveedor}?",
            "Confirmar eliminación",
            wx.YES_NO|wx.ICON_QUESTION
        )
        if confirm != wx.YES:
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proveedor WHERE idproveedor=%s", (id_proveedor,))
            conn.commit()
            wx.MessageBox("Proveedor eliminado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar proveedor: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        valores = [self.lista.GetItem(idx, i).GetText() for i in range(4)]
        self.set_inputs(valores)

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT idproveedor, nombre, telefono, direccion FROM proveedor ORDER BY nombre")
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                for i in range(1, 4):
                    self.lista.SetItem(index, i, str(row[i]) if row[i] else "")
        except Exception as e:
            wx.MessageBox(f"Error al cargar proveedores: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()
