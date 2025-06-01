import wx
from conexion import conectar

class EmpleadoCRUD(wx.Panel):
    def __init__(self, parent, title):
        super(EmpleadoCRUD, self).__init__(parent)
        
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
        form_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        form_sizer.AddGrowableCol(1)
        
        # Campos de entrada
        labels = ["ID Empleado:", "Nombres:", "Apellidos:", "Dirección:", "Teléfono:"]
        self.inputs = []
        
        for label in labels:
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((120, -1))
            form_sizer.Add(lbl, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5)
            
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
        form_sizer.Add(wx.StaticText(form_panel), flag=wx.EXPAND)  # Espacio vacío
        form_sizer.Add(btn_panel, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        
        form_panel.SetSizer(form_sizer)
        vbox.Add(form_panel, flag=wx.EXPAND|wx.ALL, border=5)
        
        # Lista de empleados
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.lista.SetMinSize((-1, 200))
        
        columnas = ["ID", "Nombres", "Apellidos", "Dirección", "Teléfono"]
        for i, col in enumerate(columnas):
            self.lista.InsertColumn(i, col, width=120 if i == 0 else 150)
        
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)
        
        self.SetSizer(vbox)
        
        # Eventos
        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar_empleado)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar_empleado)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_empleado)
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
        self.inputs[1].SetFocus()  # Enfocar el campo de nombres

    def validar_campos(self, valores):
        if not valores[1]:  # Nombres
            wx.MessageBox("El nombre es obligatorio", "Error", wx.OK|wx.ICON_ERROR)
            self.inputs[1].SetFocus()
            return False
        if not valores[2]:  # Apellidos
            wx.MessageBox("Los apellidos son obligatorios", "Error", wx.OK|wx.ICON_ERROR)
            self.inputs[2].SetFocus()
            return False
        return True

    def agregar_empleado(self, event):
        valores = self.get_inputs()
        if not self.validar_campos(valores):
            return
        if not valores[0]:  # Validación del ID ingresado manualmente
            wx.MessageBox("El ID del empleado es obligatorio", "Error", wx.OK | wx.ICON_ERROR)
            self.inputs[0].SetFocus()
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO empleado (idempleado, nombres, apellidos, direccion, telefono) VALUES (%s, %s, %s, %s, %s)",
                (valores[0], valores[1], valores[2], valores[3], valores[4])
            )
            conn.commit()
            wx.MessageBox("Empleado agregado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al agregar empleado: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def actualizar_empleado(self, event):
        valores = self.get_inputs()
        if not valores[0]:  # ID
            wx.MessageBox("Seleccione un empleado para actualizar", "Error", wx.OK|wx.ICON_ERROR)
            return
        if not self.validar_campos(valores):
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE empleado SET nombres=%s, apellidos=%s, direccion=%s, telefono=%s 
                   WHERE idempleado=%s""",
                (valores[1], valores[2], valores[3], valores[4], valores[0])
            )
            conn.commit()
            wx.MessageBox("Empleado actualizado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar empleado: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def eliminar_empleado(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion < 0:
            wx.MessageBox("Seleccione un empleado para eliminar", "Error", wx.OK|wx.ICON_ERROR)
            return
            
        id_empleado = self.lista.GetItemText(seleccion)
        
        confirm = wx.MessageBox(
            f"¿Está seguro que desea eliminar al empleado {id_empleado}?",
            "Confirmar eliminación", 
            wx.YES_NO|wx.ICON_QUESTION
        )
        
        if confirm != wx.YES:
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleado WHERE idempleado=%s", (id_empleado,))
            conn.commit()
            wx.MessageBox("Empleado eliminado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar empleado: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        valores = [self.lista.GetItem(idx, i).GetText() for i in range(5)]
        self.set_inputs(valores)

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT idempleado, nombres, apellidos, direccion, telefono FROM empleado ORDER BY apellidos, nombres")
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                for i in range(1, 5):
                    self.lista.SetItem(index, i, str(row[i]) if row[i] else "")
        except Exception as e:
            wx.MessageBox(f"Error al cargar empleados: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()