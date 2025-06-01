
import wx
from conexion import conectar

class DetalleVentaCRUD(wx.Panel):
    def __init__(self, parent, title):
        super(DetalleVentaCRUD, self).__init__(parent)
        self.SetBackgroundColour(wx.WHITE)

        vbox = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(self, label=title)
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

        labels = ["ID Detalle Venta:", "ID Venta:", "Cantidad:", "Código Producto:"]
        self.inputs = []

        for label in labels:
            lbl = wx.StaticText(form_panel, label=label)
            lbl.SetMinSize((130, -1))
            form_sizer.Add(lbl, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, border=5)
            txt = wx.TextCtrl(form_panel)
            self.inputs.append(txt)
            form_sizer.Add(txt, flag=wx.EXPAND|wx.RIGHT, border=5)

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

        self.lista = wx.ListCtrl(self, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.lista.SetMinSize((-1, 200))
        columnas = ["ID Detalle", "ID Venta", "Cantidad", "Producto Código"]
        for i, col in enumerate(columnas):
            self.lista.InsertColumn(i, col, width=140)

        vbox.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(vbox)

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

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM detalle_venta")
            for row in cursor.fetchall():
                index = self.lista.InsertItem(self.lista.GetItemCount(), str(row[0]))
                for i in range(1, 4):
                    self.lista.SetItem(index, i, str(row[i]) if row[i] else "")
        except Exception as e:
            wx.MessageBox(f"Error al cargar datos: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def agregar(self, event):
        valores = self.get_inputs()
        if all(valores):
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO detalle_venta VALUES (%s, %s, %s, %s)", valores)
                conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
            except Exception as e:
                wx.MessageBox(f"Error al agregar: {e}", "Error", wx.ICON_ERROR)
            finally:
                if conn:
                    conn.close()

    def actualizar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            valores = self.get_inputs()
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("UPDATE detalle_venta SET id_venta=%s, cantidad=%s, producto_codigo=%s WHERE id_detalle=%s",
                               (valores[1], valores[2], valores[3], valores[0]))
                conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
            except Exception as e:
                wx.MessageBox(f"Error al actualizar: {e}", "Error", wx.ICON_ERROR)
            finally:
                if conn:
                    conn.close()

    def eliminar(self, event):
        idx = self.lista.GetFirstSelected()
        if idx >= 0:
            id_detalle = self.lista.GetItemText(idx)
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM detalle_venta WHERE id_detalle=%s", (id_detalle,))
                conn.commit()
                self.actualizar_lista()
                self.limpiar_campos()
            except Exception as e:
                wx.MessageBox(f"Error al eliminar: {e}", "Error", wx.ICON_ERROR)
            finally:
                if conn:
                    conn.close()

    def seleccionar_item(self, event):
        idx = event.GetIndex()
        valores = [self.lista.GetItem(idx, i).GetText() for i in range(4)]
        self.set_inputs(valores)

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, title="CRUD Detalle Venta", size=(750, 500))
    panel = DetalleVentaCRUD(frame, "CRUD Detalle Venta")
    frame.Show()
    app.MainLoop()
