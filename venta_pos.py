import wx
import wx.adv
import cv2
from pyzbar.pyzbar import decode
from conexion import conectar
from datetime import datetime
from reportlab.pdfgen import canvas
import threading
import numpy as np

class VentaPOS(wx.Panel):
    def __init__(self, parent, id_empleado):
        self.id_empleado = id_empleado
        super().__init__(parent)
        self.SetBackgroundColour(wx.WHITE)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Panel izquierdo (30%)
        left_panel = wx.Panel(self)
        left_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Sección de cliente
        client_box = wx.StaticBox(left_panel, label="Datos del Cliente")
        client_sizer = wx.StaticBoxSizer(client_box, wx.VERTICAL)

        # Campo para buscar cliente con autocompletado
        self.txt_buscar_cliente = wx.SearchCtrl(client_box, style=wx.TE_PROCESS_ENTER)
        self.txt_buscar_cliente.SetDescriptiveText("Buscar cliente por ID o nombre")
        self.txt_buscar_cliente.Bind(wx.EVT_TEXT, self.on_buscar_cliente_text)
        client_sizer.Add(self.txt_buscar_cliente, flag=wx.EXPAND|wx.ALL, border=5)

        # Lista de sugerencias de clientes
        self.lista_sugerencias_clientes = wx.ListBox(client_box, style=wx.LB_SINGLE)
        self.lista_sugerencias_clientes.Hide()
        client_sizer.Add(self.lista_sugerencias_clientes, 1, flag=wx.EXPAND|wx.ALL, border=5)
        
        # Botón para buscar cliente
        self.btn_buscar_cliente = wx.Button(client_box, label="Buscar Cliente")
        self.btn_buscar_cliente.SetBackgroundColour(wx.Colour(0, 114, 198))
        self.btn_buscar_cliente.SetForegroundColour(wx.WHITE)
        client_sizer.Add(self.btn_buscar_cliente, flag=wx.EXPAND|wx.ALL, border=5)

        # Información del cliente
        self.cliente_info = wx.StaticText(client_box, label="Cliente: GENERAL")
        client_sizer.Add(self.cliente_info, flag=wx.EXPAND|wx.ALL, border=5)

        left_sizer.Add(client_sizer, flag=wx.EXPAND|wx.ALL, border=5)

        # Sección de búsqueda de producto
        product_box = wx.StaticBox(left_panel, label="Agregar Producto")
        product_sizer = wx.StaticBoxSizer(product_box, wx.VERTICAL)

        # Campo para código de producto con autocompletado
        self.txt_codigo = wx.SearchCtrl(product_box, style=wx.TE_PROCESS_ENTER)
        self.txt_codigo.SetDescriptiveText("Código o nombre del producto")
        self.txt_codigo.Bind(wx.EVT_TEXT, self.on_buscar_producto_text)
        product_sizer.Add(wx.StaticText(product_box, label="Código del Producto:"), flag=wx.TOP, border=5)
        product_sizer.Add(self.txt_codigo, flag=wx.EXPAND|wx.ALL, border=5)

        # Lista de sugerencias de productos
        self.lista_sugerencias_productos = wx.ListBox(product_box, style=wx.LB_SINGLE)
        self.lista_sugerencias_productos.Hide()
        product_sizer.Add(self.lista_sugerencias_productos, 1, flag=wx.EXPAND|wx.ALL, border=5)

        # Campo para cantidad
        self.txt_cantidad = wx.SpinCtrl(product_box, min=1, max=100, initial=1)
        product_sizer.Add(wx.StaticText(product_box, label="Cantidad:"), flag=wx.TOP, border=5)
        product_sizer.Add(self.txt_cantidad, flag=wx.EXPAND|wx.ALL, border=5)

        # Botón para agregar producto
        self.btn_agregar = wx.Button(product_box, label="Agregar Producto")
        self.btn_agregar.SetBackgroundColour(wx.Colour(76, 175, 80))
        self.btn_agregar.SetForegroundColour(wx.WHITE)
        product_sizer.Add(self.btn_agregar, flag=wx.EXPAND|wx.ALL, border=5)

        # Botón para escanear código de barras
        self.btn_escanear = wx.Button(product_box, label="Escanear Código de Barras")
        self.btn_escanear.SetBackgroundColour(wx.Colour(255, 193, 7))
        product_sizer.Add(self.btn_escanear, flag=wx.EXPAND|wx.ALL, border=5)

        left_sizer.Add(product_sizer, flag=wx.EXPAND|wx.ALL, border=5)

        # Sección de información
        info_box = wx.StaticBox(left_panel, label="Información")
        info_sizer = wx.StaticBoxSizer(info_box, wx.VERTICAL)

        self.fecha_hora = wx.StaticText(info_box, label=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        info_sizer.Add(wx.StaticText(info_box, label="Fecha/Hora:"), flag=wx.TOP, border=5)
        info_sizer.Add(self.fecha_hora, flag=wx.EXPAND|wx.ALL, border=5)

        left_sizer.Add(info_sizer, flag=wx.EXPAND|wx.ALL, border=5)

        left_panel.SetSizer(left_sizer)
        main_sizer.Add(left_panel, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        # Panel central (50%)
        center_panel = wx.Panel(self)
        center_sizer = wx.BoxSizer(wx.VERTICAL)

        self.lista = wx.ListCtrl(center_panel, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
        self.lista.SetMinSize((-1, 400))
        columns = ["ID", "Producto", "Precio Unit.", "Cantidad", "Subtotal", ""]
        widths = [80, 250, 100, 80, 100, 80]
        for idx, (col, width) in enumerate(zip(columns, widths)):
            self.lista.InsertColumn(idx, col, width=width)

        center_sizer.Add(self.lista, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        center_panel.SetSizer(center_sizer)
        main_sizer.Add(center_panel, proportion=2, flag=wx.EXPAND|wx.ALL, border=5)

        # Panel derecho (20%)
        right_panel = wx.Panel(self)
        right_panel.SetBackgroundColour(wx.Colour(240, 240, 240))
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        total_box = wx.StaticBox(right_panel, label="Total")
        total_sizer = wx.StaticBoxSizer(total_box, wx.VERTICAL)

        self.total_label = wx.StaticText(total_box, label="$0.00")
        font = self.total_label.GetFont()
        font.PointSize += 10
        font = font.Bold()
        self.total_label.SetFont(font)
        total_sizer.Add(self.total_label, flag=wx.ALIGN_CENTER|wx.ALL, border=10)

        right_sizer.Add(total_sizer, flag=wx.EXPAND|wx.ALL, border=5)

        # Selector de método de pago
        metodo_pago_box = wx.StaticBox(right_panel, label="Método de Pago")
        metodo_pago_sizer = wx.StaticBoxSizer(metodo_pago_box, wx.VERTICAL)

        self.selector_pago = wx.Choice(right_panel, choices=["Efectivo", "Tarjeta"])
        self.selector_pago.SetSelection(0)  # Selecciona 'Efectivo' por defecto

        metodo_pago_sizer.Add(self.selector_pago, flag=wx.EXPAND | wx.ALL, border=5)
        right_sizer.Add(metodo_pago_sizer, flag=wx.EXPAND | wx.ALL, border=5)

        self.btn_pagar = wx.Button(right_panel, label="Pagar", size=(-1, 50))
        self.btn_pagar.SetBackgroundColour(wx.Colour(0, 150, 136))
        self.btn_pagar.SetForegroundColour(wx.WHITE)
        right_sizer.Add(self.btn_pagar, flag=wx.EXPAND|wx.ALL, border=5)

        self.btn_cancelar = wx.Button(right_panel, label="Cancelar", size=(-1, 50))
        self.btn_cancelar.SetBackgroundColour(wx.Colour(244, 67, 54))
        self.btn_cancelar.SetForegroundColour(wx.WHITE)
        right_sizer.Add(self.btn_cancelar, flag=wx.EXPAND|wx.ALL, border=5)

        right_panel.SetSizer(right_sizer)
        main_sizer.Add(right_panel, proportion=1, flag=wx.EXPAND|wx.ALL, border=5)

        self.SetSizer(main_sizer)

        # Eventos
        self.btn_buscar_cliente.Bind(wx.EVT_BUTTON, self.buscar_cliente)
        self.txt_buscar_cliente.Bind(wx.EVT_TEXT_ENTER, self.buscar_cliente)
        self.lista_sugerencias_clientes.Bind(wx.EVT_LISTBOX, self.seleccionar_cliente)
        self.btn_agregar.Bind(wx.EVT_BUTTON, self.agregar_producto)
        self.txt_codigo.Bind(wx.EVT_TEXT_ENTER, self.agregar_producto)
        self.lista_sugerencias_productos.Bind(wx.EVT_LISTBOX, self.seleccionar_producto)
        self.btn_pagar.Bind(wx.EVT_BUTTON, self.finalizar_venta)
        self.btn_cancelar.Bind(wx.EVT_BUTTON, self.cancelar_venta)
        self.btn_escanear.Bind(wx.EVT_BUTTON, self.iniciar_escaneo)

        self.carrito = []
        self.cliente_actual = None
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.actualizar_reloj, self.timer)
        self.timer.Start(1000)
        
        # Variables para la cámara
        self.captura = None
        self.escaneando = False
        self.dialogo_camara = None

    def actualizar_reloj(self, event):
        self.fecha_hora.SetLabel(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def on_buscar_cliente_text(self, event):
        texto = self.txt_buscar_cliente.GetValue().strip()
        if len(texto) < 2:  # Mínimo 2 caracteres para buscar
            self.lista_sugerencias_clientes.Hide()
            self.Layout()
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            query = """
                SELECT idcliente, nombre, telefono 
                FROM cliente 
                WHERE nombre LIKE %s OR idcliente LIKE %s
                LIMIT 10
            """
            cursor.execute(query, (f"%{texto}%", f"%{texto}%"))
            
            resultados = cursor.fetchall()
            if resultados:
                self.lista_sugerencias_clientes.Clear()
                for idcliente, nombre, telefono in resultados:
                    self.lista_sugerencias_clientes.Append(f"{idcliente} - {nombre} ({telefono})", idcliente)
                self.lista_sugerencias_clientes.Show()
                self.Layout()
            else:
                self.lista_sugerencias_clientes.Hide()
                self.Layout()
                
        except Exception as e:
            wx.LogError(f"Error al buscar clientes: {str(e)}")
        finally:
            if conn:
                conn.close()

    def seleccionar_cliente(self, event):
        id_cliente = self.lista_sugerencias_clientes.GetClientData(event.GetSelection())
        self.buscar_cliente_por_id(id_cliente)
        self.lista_sugerencias_clientes.Hide()
        self.Layout()

    def buscar_cliente_por_id(self, id_cliente):
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT idcliente, nombre, direccion, telefono 
                FROM cliente 
                WHERE idcliente = %s
            """, (id_cliente,))
            
            resultado = cursor.fetchone()
            if resultado:
                id_cliente, nombre, direccion, telefono = resultado
                self.cliente_actual = {
                    'id': id_cliente,
                    'nombre': nombre,
                    'direccion': direccion,
                    'telefono': telefono
                }
                self.cliente_info.SetLabel(f"Cliente: {nombre}\nTel: {telefono}")
                self.txt_buscar_cliente.SetValue(f"{id_cliente} - {nombre}")
                
        except Exception as e:
            wx.MessageBox(f"Error al cargar cliente: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def buscar_cliente(self, event):
        texto = self.txt_buscar_cliente.GetValue().strip()
        if not texto:
            wx.MessageBox("Ingrese un ID o nombre de cliente", "Aviso", wx.OK|wx.ICON_INFORMATION)
            return
            
        # Si el texto es un ID (número)
        if texto.isdigit():
            self.buscar_cliente_por_id(int(texto))
        else:
            # Mostrar sugerencias si no es un ID
            self.on_buscar_cliente_text(event)

    def on_buscar_producto_text(self, event):
        texto = self.txt_codigo.GetValue().strip()
        if len(texto) < 2:  # Mínimo 2 caracteres para buscar
            self.lista_sugerencias_productos.Hide()
            self.Layout()
            return
            
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            query = """
                SELECT codigo, nombre, precio, codigo_barras 
                FROM producto 
                WHERE nombre LIKE %s OR codigo LIKE %s OR codigo_barras LIKE %s
                LIMIT 10
            """
            cursor.execute(query, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
            
            resultados = cursor.fetchall()
            if resultados:
                self.lista_sugerencias_productos.Clear()
                for codigo, nombre, precio, codigo_barras in resultados:
                    display_text = f"{codigo} - {nombre} (${precio:.2f})"
                    if codigo_barras:
                        display_text += f" [CB: {codigo_barras}]"
                    self.lista_sugerencias_productos.Append(display_text, codigo)
                self.lista_sugerencias_productos.Show()
                self.Layout()
            else:
                self.lista_sugerencias_productos.Hide()
                self.Layout()
                
        except Exception as e:
            wx.LogError(f"Error al buscar productos: {str(e)}")
        finally:
            if conn:
                conn.close()

    def seleccionar_producto(self, event):
        codigo_producto = self.lista_sugerencias_productos.GetClientData(event.GetSelection())
        self.txt_codigo.SetValue(str(codigo_producto))
        self.lista_sugerencias_productos.Hide()
        self.Layout()
        self.agregar_producto(None)  # None como event para que no falle

    def agregar_producto(self, event):
        codigo = self.txt_codigo.GetValue().strip()
        cantidad = self.txt_cantidad.GetValue()
        
        if not codigo:
            wx.MessageBox("Ingrese un código de producto", "Aviso", wx.OK|wx.ICON_INFORMATION)
            return
            
        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                wx.MessageBox("La cantidad debe ser mayor a cero", "Error", wx.OK|wx.ICON_ERROR)
                return
                
            conn = conectar()
            cursor = conn.cursor()
            
            # Buscar producto por código o código de barras
            cursor.execute("""
                SELECT codigo, nombre, precio, stock 
                FROM producto 
                WHERE codigo = %s OR codigo_barras = %s
                LIMIT 1
            """, (codigo, codigo))
            
            producto = cursor.fetchone()
            if not producto:
                wx.MessageBox("Producto no encontrado", "Error", wx.OK|wx.ICON_ERROR)
                return
                
            codigo, nombre, precio, stock = producto
            
            # Verificar stock
            if stock < cantidad:
                wx.MessageBox(f"No hay suficiente stock. Disponible: {stock}", "Error", wx.OK|wx.ICON_ERROR)
                return
                
            # Verificar si ya está en el carrito
            for idx, item in enumerate(self.carrito):
                if item['codigo'] == codigo:
                    # Actualizar cantidad si ya existe
                    nueva_cantidad = item['cantidad'] + cantidad
                    if nueva_cantidad > stock:
                        wx.MessageBox(f"No hay suficiente stock. Disponible: {stock}", "Error", wx.OK|wx.ICON_ERROR)
                        return
                        
                    self.carrito[idx]['cantidad'] = nueva_cantidad
                    self.carrito[idx]['subtotal'] = float(precio) * nueva_cantidad
                    self.actualizar_lista()
                    self.txt_codigo.SetValue("")
                    self.txt_cantidad.SetValue("1")
                    return
            
            # Agregar nuevo producto al carrito
            self.carrito.append({
                'codigo': codigo,
                'nombre': nombre,
                'precio': float(precio),
                'cantidad': cantidad,
                'subtotal': float(precio) * cantidad
            })
            
            self.actualizar_lista()
            self.txt_codigo.SetValue("")
            self.txt_cantidad.SetValue("1")
            
        except ValueError:
            wx.MessageBox("Ingrese una cantidad válida", "Error", wx.OK|wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error al agregar producto: {str(e)}", "Error", wx.OK|wx.ICON_ERROR)
        finally:
            if conn:
                conn.close()

    def iniciar_escaneo(self, event):
        if self.escaneando:
            return
            
        self.escaneando = True
        self.dialogo_camara = wx.Dialog(self, title="Escanear Código de Barras", size=(640, 480))
        
        panel = wx.Panel(self.dialogo_camara)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.video_panel = wx.Panel(panel)
        self.video_panel.SetMinSize((640, 480))
        sizer.Add(self.video_panel, 1, wx.EXPAND)
        
        btn_cancelar = wx.Button(panel, label="Cancelar")
        btn_cancelar.Bind(wx.EVT_BUTTON, self.detener_escaneo)
        sizer.Add(btn_cancelar, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        panel.SetSizer(sizer)
        self.dialogo_camara.Show()
        
        # Iniciar la cámara en un hilo separado
        self.captura = cv2.VideoCapture(0)
        self.hilo_escaneo = threading.Thread(target=self.escaneo_barras)
        self.hilo_escaneo.daemon = True
        self.hilo_escaneo.start()

    def escaneo_barras(self):
        while self.escaneando:
            ret, frame = self.captura.read()
            if ret:
                # Convertir a RGB para mostrar en wxPython
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width = frame_rgb.shape[:2]
                
                # Detectar códigos de barras
                codigos = decode(frame_rgb)
                for codigo in codigos:
                    data = codigo.data.decode('utf-8')
                    tipo = codigo.type
                    
                    # Dibujar rectángulo alrededor del código
                    pts = np.array([codigo.polygon], np.int32)
                    pts = pts.reshape((-1,1,2))
                    cv2.polylines(frame_rgb, [pts], True, (0,255,0), 3)
                    
                    # Mostrar el código detectado
                    cv2.putText(frame_rgb, f"{tipo}: {data}", 
                               (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.8, (0,255,0), 2)
                    
                    # Procesar el código encontrado
                    wx.CallAfter(self.procesar_codigo_barras, data)
                
                # Mostrar el frame en el panel
                wx_image = wx.Image(width, height, frame_rgb.tobytes())
                wx_bitmap = wx_image.ConvertToBitmap()
                wx.CallAfter(self.mostrar_frame, wx_bitmap)
                
        # Liberar la cámara al terminar
        self.captura.release()

    def mostrar_frame(self, bitmap):
        if not self.escaneando or not self.dialogo_camara:
            return
            
        # Crear un DC para dibujar en el panel
        dc = wx.ClientDC(self.video_panel)
        dc.DrawBitmap(bitmap, 0, 0)

    def procesar_codigo_barras(self, codigo):
        self.txt_codigo.SetValue(codigo)
        self.detener_escaneo()
        self.agregar_producto(None)

    def detener_escaneo(self, event=None):
        if self.escaneando:
            self.escaneando = False
            if self.dialogo_camara:
                self.dialogo_camara.Destroy()
                self.dialogo_camara = None
            if self.captura:
                self.captura.release()
    def eliminar_producto(self, index):
        if 0 <= index < len(self.carrito):
            del self.carrito[index]
            self.actualizar_lista()

    def actualizar_lista(self):
        self.lista.DeleteAllItems()
        total = 0
        for idx, item in enumerate(self.carrito):
            index = self.lista.InsertItem(self.lista.GetItemCount(), str(item['codigo']))
            self.lista.SetItem(index, 1, item['nombre'])
            self.lista.SetItem(index, 2, f"{item['precio']:.2f}")
            self.lista.SetItem(index, 3, str(item['cantidad']))
            self.lista.SetItem(index, 4, f"{item['subtotal']:.2f}")
            total += item['subtotal']
        self.total_label.SetLabel(f"${total:.2f}")

    def finalizar_venta(self, event):
        if not self.carrito:
            wx.MessageBox("No hay productos en el carrito", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return

        # Validar cliente
        id_cliente = 999
        if self.cliente_actual and 'id' in self.cliente_actual:
            id_cliente = self.cliente_actual['id']

        # Calcular total
        total = sum(item['subtotal'] for item in self.carrito)

        # Obtener método de pago seleccionado
        metodo_pago = self.selector_pago.GetStringSelection()

        if not metodo_pago:
            wx.MessageBox("Debe seleccionar un método de pago", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            conn = conectar()
            cursor = conn.cursor()

            # Insertar venta
            cursor.execute(
                "INSERT INTO venta (total, idcliente, id_empleado) VALUES (%s, %s, %s)",
                (total, id_cliente, self.id_empleado)
            )
            id_venta = cursor.lastrowid

            # Insertar pago
            cursor.execute(
                "INSERT INTO pagos (id_venta, metodo_pago) VALUES (%s, %s)",
                (id_venta, metodo_pago)
            )

            # Insertar detalle de venta y actualizar stock
            for item in self.carrito:
                cursor.execute(
                    "INSERT INTO detalle_venta (id_venta, cantidad, producto_codigo) VALUES (%s, %s, %s)",
                    (id_venta, item['cantidad'], item['codigo'])
                )
                cursor.execute(
                    "UPDATE producto SET stock = stock - %s WHERE codigo = %s",
                    (item['cantidad'], item['codigo'])
                )

            conn.commit()
            conn.close()

            self.generar_ticket_pdf(id_venta, self.carrito, total)
            wx.MessageBox("Venta finalizada exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.cancelar_venta(None)

        except Exception as e:
            wx.MessageBox(f"Error al finalizar la venta: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def generar_ticket_pdf(self, id_venta, carrito, total):
        c = canvas.Canvas(f"ticket_venta_{id_venta}.pdf")
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 800, "TICKET DE VENTA")
        c.setFont("Helvetica", 12)
        c.drawString(50, 780, f"Venta ID: {id_venta}")
        c.drawString(50, 765, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 750, "-"*70)
        y = 730
        for item in carrito:
            c.drawString(50, y, f"{item['nombre']} x{item['cantidad']} - ${item['subtotal']:.2f}")
            y -= 20
        c.drawString(50, y-10, "-"*70)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y-40, f"TOTAL: ${total:.2f}")
        c.drawString(50, y-70, "¡Gracias por su compra!")
        c.save()

    def cancelar_venta(self, event):
        self.carrito = []
        self.actualizar_lista()
        self.txt_codigo.SetValue("")
        self.txt_cantidad.SetValue(1)
        self.txt_buscar_cliente.SetValue("")
        self.cliente_info.SetLabel("Cliente: GENERAL")
        self.cliente_actual = None
