
import wx
from conexion import conectar

class ProductoPanel(wx.Panel):
    def __init__(self, parent):
        super(ProductoPanel, self).__init__(parent)
        self.SetBackgroundColour(wx.WHITE)

        vbox = wx.BoxSizer(wx.VERTICAL)
        titulo = wx.StaticText(self, label="Gestión de Productos")
        titulo.SetForegroundColour(wx.Colour(0, 64, 128))
        font = titulo.GetFont()
        font.PointSize += 6
        font = font.Bold()
        titulo.SetFont(font)
        vbox.Add(titulo, flag=wx.ALL|wx.ALIGN_CENTER, border=10)

        form_panel = wx.Panel(self)
        form_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        form_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        form_sizer.AddGrowableCol(1)

        labels = ["Código:", "Nombre:", "Descripción:", "Precio:", "Stock:", "Caducidad:", "Categoría:", "Inventario:", "Código de Barras:"]
        self.inputs = []

        for label in labels:
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((120, -1))
            form_sizer.Add(lbl, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5)
            txt = wx.TextCtrl(form_panel)
            self.inputs.append(txt)
            form_sizer.Add(txt, flag=wx.EXPAND|wx.RIGHT, border=5)

        self.imagen_codigo = None
        btn_imagen = wx.Button(form_panel, label="Seleccionar Imagen Código")
        btn_imagen.Bind(wx.EVT_BUTTON, self.seleccionar_imagen_codigo)
        form_sizer.Add(wx.StaticText(form_panel), flag=wx.EXPAND)
        form_sizer.Add(btn_imagen, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        btn_panel = wx.Panel(form_panel)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_add = wx.Button(btn_panel, label="Agregar", size=(100, 30))
        self.btn_update = wx.Button(btn_panel, label="Actualizar", size=(100, 30))
        self.btn_delete = wx.Button(btn_panel, label="Eliminar", size=(100, 30))
        self.btn_clear = wx.Button(btn_panel, label="Limpiar", size=(100, 30))

        for btn, color in [(self.btn_add, (0,128,0)), (self.btn_update, (0,0,128)), (self.btn_delete, (128,0,0)), (self.btn_clear, (128,128,0))]:
            btn.SetBackgroundColour(wx.Colour(*color))
            btn.SetForegroundColour(wx.WHITE)
            btn_sizer.Add(btn, flag=wx.RIGHT, border=5)

        btn_panel.SetSizer(btn_sizer)
        form_sizer.Add(wx.StaticText(form_panel), flag=wx.EXPAND)
        form_sizer.Add(btn_panel, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        form_panel.SetSizer(form_sizer)
        vbox.Add(form_panel, flag=wx.EXPAND|wx.ALL, border=5)

        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        columnas = ["Código", "Nombre", "Descripción", "Precio", "Stock", "Caducidad", "Categoría", "Inventario", "Código Barras"]
        for i, col in enumerate(columnas):
            self.lista.InsertColumn(i, col, width=120)
        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(vbox)

        self.btn_add.Bind(wx.EVT_BUTTON, self.agregar)
        self.btn_update.Bind(wx.EVT_BUTTON, self.actualizar)
        self.btn_delete.Bind(wx.EVT_BUTTON, self.eliminar)
        self.btn_clear.Bind(wx.EVT_BUTTON, lambda e: self.limpiar_campos())
        self.lista.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_item)

        self.actualizar_lista()

    def seleccionar_imagen_codigo(self, event):
        with wx.FileDialog(self, "Seleccionar imagen de código", wildcard="Imagenes (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            self.imagen_codigo = fileDialog.GetPath()

    def get_inputs(self):
        return [ctrl.GetValue().strip() for ctrl in self.inputs]

    def set_inputs(self, values):
        for ctrl, val in zip(self.inputs, values):
            ctrl.SetValue(str(val))
        self.imagen_codigo = None

    def limpiar_campos(self):
        for ctrl in self.inputs:
            ctrl.SetValue("")
        self.imagen_codigo = None

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre, descripcion, precio, stock, caducidad, categoria, inventario, codigo_barras FROM producto")
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                for i in range(1, len(row)):
                    self.lista.SetItem(index, i, str(row[i]) if row[i] else "")
        except Exception as e:
            wx.MessageBox(f"Error al cargar productos: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def agregar(self, event):
        valores = self.get_inputs()
        if not all(valores[:9]):
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK|wx.ICON_ERROR)
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO producto (codigo, nombre, descripcion, precio, stock, caducidad, categoria, inventario, codigo_barras)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", valores[:9]
            )
            conn.commit()
            wx.MessageBox("Producto agregado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al agregar producto: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def actualizar(self, event):
        valores = self.get_inputs()
        if not valores[0]:
            wx.MessageBox("Seleccione un producto para actualizar", "Error", wx.OK|wx.ICON_ERROR)
            return
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE producto SET nombre=%s, descripcion=%s, precio=%s, stock=%s, caducidad=%s, 
                categoria=%s, inventario=%s, codigo_barras=%s WHERE codigo=%s""",
                (valores[1], valores[2], valores[3], valores[4], valores[5], valores[6], valores[7], valores[8], valores[0])
            )
            conn.commit()
            wx.MessageBox("Producto actualizado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar producto: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx < 0:
            wx.MessageBox("Seleccione un producto para eliminar", "Error", wx.OK|wx.ICON_ERROR)
            return
        codigo = self.lista.GetItemText(idx)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM producto WHERE codigo=%s", (codigo,))
            conn.commit()
            wx.MessageBox("Producto eliminado correctamente", "Éxito", wx.OK|wx.ICON_INFORMATION)
            self.actualizar_lista()
            self.limpiar_campos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar producto: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        valores = [self.lista.GetItem(idx, i).GetText() for i in range(9)]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="Gestión de Productos", size=(1000, 600))
    panel = ProductoPanel(frame)
    frame.Show()
    app.MainLoop()
