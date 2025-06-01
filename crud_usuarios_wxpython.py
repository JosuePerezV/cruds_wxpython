import wx
from conexion import conectar

class UsuarioCRUD(wx.Panel):
    def __init__(self, parent, title="Gestión de Usuarios"):
        super().__init__(parent)
        self.SetBackgroundColour(wx.WHITE)

        vbox = wx.BoxSizer(wx.VERTICAL)

        # Título
        titulo = wx.StaticText(self, label=title)
        titulo.SetForegroundColour(wx.Colour(0, 64, 128))
        font = titulo.GetFont()
        font.PointSize += 6
        font = font.Bold()
        titulo.SetFont(font)
        vbox.Add(titulo, flag=wx.ALL | wx.ALIGN_CENTER, border=10)

        # Panel de formulario
        form_panel = wx.Panel(self)
        form_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        form_sizer = wx.BoxSizer(wx.VERTICAL)

        # Campos
        self.txt_id = wx.TextCtrl(form_panel, style=wx.TE_READONLY)
        self.cmb_empleado = wx.ComboBox(form_panel, style=wx.CB_READONLY)
        self.txt_usuario = wx.TextCtrl(form_panel)
        self.txt_contrasena = wx.TextCtrl(form_panel, style=wx.TE_PASSWORD)
        self.cmb_cargo = wx.ComboBox(form_panel, style=wx.CB_READONLY)
        self.cmb_cargo.AppendItems(["Administrador", "Cajero", "Otro"])

        campos = [
            ("ID Usuario:", self.txt_id),
            ("Empleado:", self.cmb_empleado),
            ("Usuario:", self.txt_usuario),
            ("Contraseña:", self.txt_contrasena),
            ("Cargo:", self.cmb_cargo)
        ]

        for label, ctrl in campos:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((120, -1))
            hbox.Add(lbl, flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=8)
            hbox.Add(ctrl, proportion=1, flag=wx.EXPAND)
            form_sizer.Add(hbox, flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_panel = wx.Panel(form_panel)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_add = wx.Button(btn_panel, label="Agregar", size=(100, 30))
        self.btn_update = wx.Button(btn_panel, label="Actualizar", size=(100, 30))
        self.btn_delete = wx.Button(btn_panel, label="Eliminar", size=(100, 30))
        self.btn_limpiar = wx.Button(btn_panel, label="Limpiar", size=(100, 30))

        self.btn_add.SetBackgroundColour(wx.Colour(0, 128, 0))
        self.btn_add.SetForegroundColour(wx.WHITE)
        self.btn_update.SetBackgroundColour(wx.Colour(0, 0, 128))
        self.btn_update.SetForegroundColour(wx.WHITE)
        self.btn_delete.SetBackgroundColour(wx.Colour(128, 0, 0))
        self.btn_delete.SetForegroundColour(wx.WHITE)
        self.btn_limpiar.SetBackgroundColour(wx.Colour(128, 128, 0))
        self.btn_limpiar.SetForegroundColour(wx.WHITE)

        btn_sizer.Add(self.btn_add, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_update, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_delete, flag=wx.RIGHT, border=5)
        btn_sizer.Add(self.btn_limpiar)

        btn_panel.SetSizer(btn_sizer)
        form_sizer.Add(btn_panel, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        form_panel.SetSizer(form_sizer)
        vbox.Add(form_panel, flag=wx.EXPAND | wx.ALL, border=5)

        # Lista de usuarios
        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista.SetMinSize((-1, 200))
        self.lista.InsertColumn(0, "ID Usuario", width=100)
        self.lista.InsertColumn(1, "Empleado", width=200)
        self.lista.InsertColumn(2, "Usuario", width=150)
        self.lista.InsertColumn(3, "Cargo", width=120)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        self.SetSizer(vbox)

        # Eventos
        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar)
        self.btn_limpiar.Bind(wx.EVT_BUTTON, lambda e: self.limpiar_campos())
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)

        self.empleado_map = {}
        self.cargar_empleados()
        self.actualizar_lista()

    def cargar_empleados(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT idempleado, CONCAT(nombres, ' ', apellidos) FROM empleado")
            self.empleado_map.clear()
            self.cmb_empleado.Clear()
            for ide, nombre in cursor.fetchall():
                self.empleado_map[nombre] = ide
                self.cmb_empleado.Append(nombre)
        except Exception as e:
            wx.MessageBox(f"Error al cargar empleados: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def get_inputs(self):
        return (
            self.txt_id.GetValue(),
            self.empleado_map.get(self.cmb_empleado.GetValue(), None),
            self.txt_usuario.GetValue(),
            self.txt_contrasena.GetValue(),
            self.cmb_cargo.GetValue()
        )

    def limpiar_campos(self):
        self.txt_id.SetValue("")
        self.cmb_empleado.SetSelection(-1)
        self.txt_usuario.SetValue("")
        self.txt_contrasena.SetValue("")
        self.cmb_cargo.SetSelection(-1)

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id_usuario, CONCAT(e.nombres, ' ', e.apellidos), u.usuario, u.cargo
                FROM usuarios u
                JOIN empleado e ON u.id_empleado = e.idempleado
                ORDER BY u.usuario
            """)
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                self.lista.SetItem(index, 1, str(row[1]))
                self.lista.SetItem(index, 2, str(row[2]))
                self.lista.SetItem(index, 3, str(row[3]))
        except Exception as e:
            wx.MessageBox(f"Error al cargar usuarios: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def agregar(self, event):
        _, id_empleado, usuario, contrasena, cargo = self.get_inputs()

        if not id_empleado or not usuario or not contrasena or not cargo:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (id_empleado, usuario, contrasena, cargo) VALUES (%s, %s, %s, %s)",
                (id_empleado, usuario, contrasena, cargo)
            )
            conn.commit()
            wx.MessageBox("Usuario agregado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al agregar usuario: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def actualizar(self, event):
        id_usuario, id_empleado, usuario, contrasena, cargo = self.get_inputs()

        if not id_usuario or not id_empleado or not usuario or not cargo:
            wx.MessageBox("Todos los campos obligatorios deben estar completos", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            if contrasena:
                cursor.execute("""
                    UPDATE usuarios 
                    SET id_empleado=%s, usuario=%s, contrasena=%s, cargo=%s 
                    WHERE id_usuario=%s
                """, (id_empleado, usuario, contrasena, cargo, id_usuario))
            else:
                cursor.execute("""
                    UPDATE usuarios 
                    SET id_empleado=%s, usuario=%s, cargo=%s
                    WHERE id_usuario=%s
                """, (id_empleado, usuario, cargo, id_usuario))
            conn.commit()
            wx.MessageBox("Usuario actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.actualizar_lista()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar usuario: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def eliminar(self, event):
        seleccion = self.lista.GetFirstSelected()
        if seleccion < 0:
            wx.MessageBox("Seleccione un usuario para eliminar", "Error", wx.OK | wx.ICON_ERROR)
            return

        id_usuario = self.lista.GetItemText(seleccion)
        confirm = wx.MessageBox(
            f"¿Está seguro que desea eliminar el usuario {id_usuario}?",
            "Confirmar eliminación",
            wx.YES_NO | wx.ICON_QUESTION
        )
        if confirm != wx.YES:
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
            conn.commit()
            wx.MessageBox("Usuario eliminado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar usuario: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        id_usuario = self.lista.GetItemText(idx)
        nombre_empleado = self.lista.GetItem(idx, 1).GetText()
        usuario = self.lista.GetItem(idx, 2).GetText()
        cargo = self.lista.GetItem(idx, 3).GetText()

        self.txt_id.SetValue(id_usuario)
        self.cmb_empleado.SetValue(nombre_empleado)
        self.txt_usuario.SetValue(usuario)
        self.cmb_cargo.SetValue(cargo)
        self.txt_contrasena.SetValue("")  # Nunca mostrar contraseña


if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="CRUD Usuarios", size=(720, 520))
    panel = UsuarioCRUD(frame)
    frame.Show()
    app.MainLoop()
