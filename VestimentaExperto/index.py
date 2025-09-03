from clips import Environment
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaRecomendacion:
    def __init__(self, parent, datos, recomendaciones):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Recomendación de Vestimenta")
        self.ventana.geometry("500x400")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.resizable(False, False)
        
        # Centrar la ventana
        self.ventana.transient(parent)
        self.ventana.grab_set()
        
        # Título principal
        titulo = tk.Label(self.ventana, text="RECOMENDACIÓN PERSONALIZADA", 
                         font=("Arial", 14, "bold"), bg='#f8f9fa', fg='#2c3e50')
        titulo.pack(pady=15)
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Canvas y scrollbar para contenido scrolleable
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Sección de condiciones analizadas
        condiciones_frame = tk.LabelFrame(scrollable_frame, text="Condiciones Analizadas", 
                                        font=("Arial", 11, "bold"), bg='#e3f2fd', 
                                        fg='#1565c0', padx=15, pady=10)
        condiciones_frame.pack(fill="x", pady=(0, 15))
        
        condiciones_text = f"""Temperatura: {datos['temperatura']}°C
Viento: {datos['viento'].capitalize()}
Lluvia: {datos['lluvia'].capitalize()}  
Humedad: {datos['humedad'].capitalize()}
Contexto: {datos['contexto'].capitalize()}
Estación: {datos['estacion'].capitalize()}"""
        
        tk.Label(condiciones_frame, text=condiciones_text, font=("Arial", 10), 
                bg='#e3f2fd', justify="left").pack(anchor="w")
        
        # Sección de recomendaciones
        rec_frame = tk.LabelFrame(scrollable_frame, text="Recomendaciones", 
                                font=("Arial", 11, "bold"), bg='#e8f5e8', 
                                fg='#2e7d32', padx=15, pady=10)
        rec_frame.pack(fill="x", pady=(0, 15))
        
        if recomendaciones:
            for i, rec in enumerate(recomendaciones, 1):
                rec_label = tk.Label(rec_frame, text=f"• {rec}", 
                                   font=("Arial", 10), bg='#e8f5e8', 
                                   wraplength=400, justify="left")
                rec_label.pack(anchor="w", pady=2)
        else:
            # Recomendación general basada en temperatura
            if datos['temperatura'] > 25:
                rec_general = "• Usa ropa ligera y fresca"
            elif datos['temperatura'] < 15:
                rec_general = "• Usa ropa abrigada"
            else:
                rec_general = "• Usa ropa cómoda para clima templado"
                
            tk.Label(rec_frame, text="No se activaron reglas específicas", 
                    font=("Arial", 10, "italic"), bg='#e8f5e8').pack(anchor="w")
            tk.Label(rec_frame, text=rec_general, font=("Arial", 10), 
                    bg='#e8f5e8').pack(anchor="w", pady=(5,0))
        
        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        button_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        button_frame.pack(fill="x", padx=20, pady=10)
        
        btn_nuevo = tk.Button(button_frame, text="Nueva Consulta", 
                            command=self.nueva_consulta,
                            font=("Arial", 10, "bold"), bg='#4caf50', fg='white',
                            padx=20, pady=8, cursor="hand2")
        btn_nuevo.pack(side="left", padx=(0, 10))
        
        btn_cerrar = tk.Button(button_frame, text="Cerrar", 
                             command=self.ventana.destroy,
                             font=("Arial", 10, "bold"), bg='#f44336', fg='white',
                             padx=20, pady=8, cursor="hand2")
        btn_cerrar.pack(side="right")
        
        # Centrar la ventana en la pantalla
        self.centrar_ventana()
        
    def centrar_ventana(self):
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')
    
    def nueva_consulta(self):
        self.ventana.destroy()

class SistemaExpertoVestimenta:
    def __init__(self):
        self.env = Environment()
        self.configurar_sistema_experto()
        self.crear_interfaz()
        
    def configurar_sistema_experto(self):
        # Template simplificado
        self.env.build("""
        (deftemplate clima
           (slot temperatura (type NUMBER))
           (slot viento (type SYMBOL))
           (slot lluvia (type SYMBOL))
           (slot humedad (type SYMBOL))
           (slot contexto (type SYMBOL))
           (slot estacion (type SYMBOL)))
        """)
        
        # Template para recomendaciones
        self.env.build("""
        (deftemplate recomendacion
           (slot texto (type STRING)))
        """)
        
        # Reglas del sistema experto
        reglas = [
            """
            (defrule calor-extremo
                (clima (temperatura ?t&:(> ?t 32)))
                =>
                (assert (recomendacion (texto "Usa ropa muy ligera: camiseta y short"))))
            """,
            
            """
            (defrule soleado-calor
                (clima (lluvia no) (temperatura ?t&:(> ?t 28)))
                =>
                (assert (recomendacion (texto "Usa camiseta, short y zapatos frescos"))))
            """,
            
            """
            (defrule humedad-calor
                (clima (humedad alta) (temperatura ?t&:(> ?t 26)))
                =>
                (assert (recomendacion (texto "Usa ropa ligera y transpirable"))))
            """,
            
            """
            (defrule formal-calor
                (clima (contexto formal) (temperatura ?t&:(> ?t 28)))
                =>
                (assert (recomendacion (texto "Usa traje ligero de lino o algodón"))))
            """,
            
            """
            (defrule templado-humedad
                (clima (temperatura ?t&:(and (>= ?t 20) (<= ?t 25))) (humedad alta))
                =>
                (assert (recomendacion (texto "Usa ropa ligera y transpirable"))))
            """,
            
            """
            (defrule soleado-agradable
                (clima (lluvia no) (temperatura ?t&:(and (>= ?t 18) (<= ?t 25))))
                =>
                (assert (recomendacion (texto "Usa camiseta y jeans"))))
            """,
            
            """
            (defrule fresco
                (clima (temperatura ?t&:(and (>= ?t 12) (<= ?t 18))))
                =>
                (assert (recomendacion (texto "Usa suéter y pantalón largo"))))
            """,
            
            """
            (defrule trabajo-templado
                (clima (contexto trabajo) (temperatura ?t&:(and (>= ?t 15) (<= ?t 22))))
                =>
                (assert (recomendacion (texto "Usa chaqueta ligera o cárdigan"))))
            """,
            
            """
            (defrule deporte-frio
                (clima (contexto deporte) (temperatura ?t&:(< ?t 15)))
                =>
                (assert (recomendacion (texto "Usa sudadera o chaqueta deportiva"))))
            """,
            
            """
            (defrule invierno-frio
                (clima (estacion invierno) (temperatura ?t&:(< ?t 12)))
                =>
                (assert (recomendacion (texto "Usa abrigo grueso y pantalón largo"))))
            """,
            
            """
            (defrule frio-viento
                (clima (temperatura ?t&:(< ?t 10)) (viento fuerte))
                =>
                (assert (recomendacion (texto "Usa abrigo grueso, bufanda y guantes"))))
            """,
            
            """
            (defrule lluvia-cualquier
                (clima (lluvia ?l&:(neq ?l no)))
                =>
                (assert (recomendacion (texto "Lleva impermeable o sombrilla"))))
            """,
            
            """
            (defrule lluvia-viento
                (clima (viento fuerte) (lluvia ?l&:(or (eq ?l fuerte) (eq ?l ligera))))
                =>
                (assert (recomendacion (texto "Usa chaqueta impermeable y botas"))))
            """,
            
            """
            (defrule lluvia-frio
                (clima (lluvia ?l&:(neq ?l no)) (temperatura ?t&:(< ?t 15)))
                =>
                (assert (recomendacion (texto "Usa saco, pantalón largo y botas"))))
            """,
            
            """
            (defrule nublado-suave
                (clima (lluvia no) (viento suave) (temperatura ?t&:(and (>= ?t 15) (<= ?t 25))))
                =>
                (assert (recomendacion (texto "Usa pantalón largo y camisa ligera"))))
            """
        ]
        
        # Construir reglas
        for regla in reglas:
            try:
                self.env.build(regla)
            except Exception as e:
                print(f"Error construyendo regla: {e}")
    
    def crear_interfaz(self):
        self.root = tk.Tk()
        self.root.title("Sistema Experto - Recomendaciones de Vestimenta")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Título
        titulo = tk.Label(self.root, text="Sistema Experto para\nrecomendaciones de vestimenta", 
                         font=("Arial", 14, "bold"), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=20)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg='#f0f0f0')
        frame_principal.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Temperatura
        tk.Label(frame_principal, text="Temperatura (°C):", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.temp_var = tk.StringVar(value=0)
        temp_entry = tk.Entry(frame_principal, textvariable=self.temp_var, font=("Arial", 10))
        temp_entry.pack(fill="x", pady=(0,10))
        
        # Viento
        tk.Label(frame_principal, text="Intensidad del Viento:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.viento_var = tk.StringVar(value="suave")
        viento_combo = ttk.Combobox(frame_principal, textvariable=self.viento_var, 
                                   values=["suave", "fuerte"], font=("Arial", 10))
        viento_combo.pack(fill="x", pady=(0,10))
        
        # Lluvia
        tk.Label(frame_principal, text="Intensidad de Lluvia:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.lluvia_var = tk.StringVar(value="no")
        lluvia_combo = ttk.Combobox(frame_principal, textvariable=self.lluvia_var, 
                                   values=["no", "ligera", "fuerte"], font=("Arial", 10))
        lluvia_combo.pack(fill="x", pady=(0,10))
        
        # Humedad
        tk.Label(frame_principal, text="Humedad:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.humedad_var = tk.StringVar(value="normal")
        humedad_combo = ttk.Combobox(frame_principal, textvariable=self.humedad_var, 
                                    values=["baja", "normal", "alta"], font=("Arial", 10))
        humedad_combo.pack(fill="x", pady=(0,10))
        
        # Contexto
        tk.Label(frame_principal, text="Contexto:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.contexto_var = tk.StringVar(value="casual")
        contexto_combo = ttk.Combobox(frame_principal, textvariable=self.contexto_var, 
                                     values=["casual", "trabajo", "formal", "deporte"], font=("Arial", 10))
        contexto_combo.pack(fill="x", pady=(0,10))
        
        # Estación
        tk.Label(frame_principal, text="Estación:", font=("Arial", 10, "bold"), 
                bg='#f0f0f0').pack(anchor="w", pady=(10,5))
        self.estacion_var = tk.StringVar(value="primavera")
        estacion_combo = ttk.Combobox(frame_principal, textvariable=self.estacion_var, 
                                     values=["primavera", "verano", "otoño", "invierno"], font=("Arial", 10))
        estacion_combo.pack(fill="x", pady=(0,10))
        
        # Botón consultar
        btn_consultar = tk.Button(frame_principal, text="Obtener Recomendación", 
                                 command=self.obtener_recomendacion, 
                                 font=("Arial", 12, "bold"), bg='#3498db', fg='white',
                                 pady=15, cursor="hand2")
        btn_consultar.pack(fill="x", pady=30)
        
        # Información adicional
        info_label = tk.Label(frame_principal, 
                            text="💡 Completa los datos y haz clic en el botón para recibir\nrecomendaciones personalizadas en una ventana emergente.",
                            font=("Arial", 9, "italic"), bg='#f0f0f0', fg='#7f8c8d')
        info_label.pack(pady=10)
    
    def obtener_recomendacion(self):
        try:
            # Validar temperatura
            temperatura = float(self.temp_var.get())
            
            # Resetear entorno
            self.env.reset()
            
            # Capturar datos
            datos = {
                'temperatura': temperatura,
                'viento': self.viento_var.get(),
                'lluvia': self.lluvia_var.get(),
                'humedad': self.humedad_var.get(),
                'contexto': self.contexto_var.get(),
                'estacion': self.estacion_var.get()
            }
            
            # Crear y ejecutar hecho
            hecho_str = f"(clima (temperatura {temperatura}) (viento {datos['viento']}) (lluvia {datos['lluvia']}) (humedad {datos['humedad']}) (contexto {datos['contexto']}) (estacion {datos['estacion']}))"
            self.env.assert_string(hecho_str)
            self.env.run()
            
            # Capturar recomendaciones
            recomendaciones = []
            for fact in self.env.facts():
                if hasattr(fact, 'template') and fact.template.name == 'recomendacion':
                    recomendaciones.append(str(fact['texto']))
            
            # Mostrar popup con resultados
            VentanaRecomendacion(self.root, datos, recomendaciones)
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa una temperatura numérica válida")
        except Exception as e:
            messagebox.showerror("Error del Sistema", f"Error inesperado: {str(e)}")
    
    def ejecutar(self):
        self.root.mainloop()

# Ejecutar la aplicación
if __name__ == "__main__":
    sistema = SistemaExpertoVestimenta()
    sistema.ejecutar()
