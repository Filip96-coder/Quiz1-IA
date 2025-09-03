import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk, messagebox

class VentanaResultadosDifuso:
    def __init__(self, parent, datos_entrada, resultado):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Resultado del Sistema Difuso")
        self.ventana.geometry("700x500")
        self.ventana.configure(bg='#f8f9fa')
        self.ventana.resizable(False, False)

        # Centrar y configurar ventana
        self.ventana.transient(parent)
        self.ventana.grab_set()

        # Título principal
        titulo = tk.Label(
            self.ventana,
            text="Recomendación de Vestimenta Difusa",
            font=("Arial", 14, "bold"),
            bg='#f8f9fa',
            fg="#023b74"
        )
        titulo.pack(pady=15)

        # Frame principal con scroll
        main_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Sección de datos de entrada
        entrada_frame = tk.LabelFrame(
            scrollable_frame,
            text="Datos de Entrada Analizados",
            font=("Arial", 11, "bold"),
            bg='#e3f2fd',
            fg='#1565c0',
            padx=15,
            pady=10
        )
        entrada_frame.pack(fill="x", pady=(0, 15))

        entrada_text = (
            f"Temperatura: {datos_entrada['temperatura']}°C\n"
            f"Humedad: {datos_entrada['humedad']}%\n"
            f"Lluvia: {self.interpretar_lluvia(datos_entrada['lluvia'])}"
        )

        tk.Label(
            entrada_frame,
            text=entrada_text,
            font=("Arial", 10),
            bg='#e3f2fd',
            justify="left"
        ).pack(anchor="w")

        # Sección de resultado difuso
        resultado_frame = tk.LabelFrame(
            scrollable_frame,
            text="Resultado del Sistema Difuso",
            font=("Arial", 11, "bold"),
            bg='#e8f5e8',
            fg='#2e7d32',
            padx=15,
            pady=10
        )
        resultado_frame.pack(fill="x", pady=(0, 15))

        # Interpretación del resultado
        interpretacion = self.interpretar_resultado(resultado)

        resultado_text = (
            f"Valor Numérico: {resultado:.2f}/10\n"
            f"Categoría: {interpretacion['categoria']}\n"
            f"Recomendación: {interpretacion['recomendacion']}\n"
            f"Descripción: {interpretacion['descripcion']}"
        )

        tk.Label(
            resultado_frame,
            text=resultado_text,
            font=("Arial", 10),
            bg='#e8f5e8',
            justify="left",
            wraplength=600
        ).pack(anchor="w")

        # Configurar scroll
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botones
        button_frame = tk.Frame(self.ventana, bg='#f8f9fa')
        button_frame.pack(fill="x", padx=20, pady=10)

        btn_nuevo = tk.Button(
            button_frame,
            text="Nueva Consulta",
            command=self.nueva_consulta,
            font=("Arial", 10, "bold"),
            bg='#4caf50',
            fg='white',
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_nuevo.pack(side="left", padx=(0, 10))

        btn_cerrar = tk.Button(
            button_frame,
            text="Cerrar",
            command=self.ventana.destroy,
            font=("Arial", 10, "bold"),
            bg='#f44336',
            fg='white',
            padx=20,
            pady=8,
            cursor="hand2"
        )
        btn_cerrar.pack(side="right")

        # Centrar ventana
        self.centrar_ventana()

    def interpretar_lluvia(self, valor):
        if valor == 0:
            return "Sin lluvia"
        elif valor == 1:
            return "Lluvia ligera"
        else:
            return "Lluvia fuerte"

    def interpretar_resultado(self, valor):
        if valor <= 2.5:
            return {
                'categoria': 'MUY LIGERA',
                'recomendacion': 'Camiseta y short',
                'descripcion': 'Ropa muy liviana, perfecta para climas cálidos y secos.'
            }
        elif valor <= 5:
            return {
                'categoria': 'LIGERA',
                'recomendacion': 'Camiseta y jeans',
                'descripcion': 'Ropa cómoda y fresca, ideal para temperaturas templadas.'
            }
        elif valor <= 7.5:
            return {
                'categoria': 'ABRIGADA',
                'recomendacion': 'Suéter y pantalón largo',
                'descripcion': 'Ropa que proporciona calor moderado para temperaturas frescas.'
            }
        else:
            return {
                'categoria': 'MUY ABRIGADA',
                'recomendacion': 'Abrigo grueso, bufanda y guantes',
                'descripcion': 'Ropa de invierno para protegerse del frío intenso y condiciones adversas.'
            }

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        width = self.ventana.winfo_width()
        height = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')

    def nueva_consulta(self):
        self.ventana.destroy()


class SistemaLogicaDifusa:
    def __init__(self):
        self.sistema_ctrl = None
        self.configurar_sistema_difuso()
        self.crear_interfaz()

    def configurar_sistema_difuso(self):
        try:
            # Variables de entrada
            self.temperatura = ctrl.Antecedent(np.arange(0, 41, 1), 'temperatura')
            self.humedad = ctrl.Antecedent(np.arange(0, 101, 1), 'humedad')
            self.lluvia = ctrl.Antecedent(np.arange(0, 3, 1), 'lluvia')

            # Variable de salida
            self.vestimenta = ctrl.Consequent(np.arange(0, 11, 1), 'vestimenta')

            # Funciones de membresía
            self.temperatura['frio'] = fuzz.trimf(self.temperatura.universe, [0, 0, 20])
            self.temperatura['templado'] = fuzz.trimf(self.temperatura.universe, [15, 25, 35])
            self.temperatura['calor'] = fuzz.trimf(self.temperatura.universe, [30, 40, 40])

            self.humedad['baja'] = fuzz.trimf(self.humedad.universe, [0, 0, 50])
            self.humedad['media'] = fuzz.trimf(self.humedad.universe, [40, 50, 80])
            self.humedad['alta'] = fuzz.trimf(self.humedad.universe, [70, 100, 100])

            self.lluvia['no'] = fuzz.trimf(self.lluvia.universe, [0, 0, 0.5])
            self.lluvia['ligera'] = fuzz.trimf(self.lluvia.universe, [0.3, 1, 1.7])
            self.lluvia['fuerte'] = fuzz.trimf(self.lluvia.universe, [1.3, 2, 2])

            self.vestimenta['muy_ligera'] = fuzz.trimf(self.vestimenta.universe, [0, 0, 3])
            self.vestimenta['ligera'] = fuzz.trimf(self.vestimenta.universe, [2, 4, 6])
            self.vestimenta['abrigada'] = fuzz.trimf(self.vestimenta.universe, [5, 7, 9])
            self.vestimenta['muy_abrigada'] = fuzz.trimf(self.vestimenta.universe, [8, 10, 10])

            # Reglas (compactadas, pero con cobertura)
            reglas = [
                ctrl.Rule(self.temperatura['frio'], self.vestimenta['abrigada']),
                ctrl.Rule(self.temperatura['templado'], self.vestimenta['ligera']),
                ctrl.Rule(self.temperatura['calor'], self.vestimenta['muy_ligera']),
                ctrl.Rule(self.lluvia['fuerte'], self.vestimenta['abrigada']),
                ctrl.Rule(self.lluvia['ligera'], self.vestimenta['ligera']),
                ctrl.Rule(self.humedad['alta'], self.vestimenta['ligera'])
            ]

            self.sistema_ctrl = ctrl.ControlSystem(reglas)
            print("Sistema difuso configurado correctamente")

        except Exception as e:
            print(f"Error configurando sistema difuso: {e}")
            raise e

    def crear_interfaz(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Lógica Difusa - Vestimenta")
        self.root.geometry("600x450")
        self.root.configure(bg='#f0f0f0')

        # Título
        titulo = tk.Label(
            self.root,
            text="Sistema de Lógica Difusa\nRecomendación de Vestimenta",
            font=("Arial", 14, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=20)

        frame_principal = tk.Frame(self.root, bg='#f0f0f0')
        frame_principal.pack(padx=20, pady=10, fill="both", expand=True)

        # Temperatura
        tk.Label(frame_principal, text="Temperatura (°C):", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor="w")
        self.temp_var = tk.StringVar()
        tk.Entry(frame_principal, textvariable=self.temp_var, font=("Arial", 10)).pack(fill="x", pady=(0,10))

        # Humedad
        tk.Label(frame_principal, text="Humedad (%):", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor="w")
        self.humedad_var = tk.StringVar()
        tk.Entry(frame_principal, textvariable=self.humedad_var, font=("Arial", 10)).pack(fill="x", pady=(0,10))

        # Lluvia
        tk.Label(frame_principal, text="Intensidad de Lluvia (0=No, 1=Ligera, 2=Fuerte):", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor="w")
        self.lluvia_var = tk.StringVar(value="0")
        ttk.Combobox(frame_principal, textvariable=self.lluvia_var, values=["0", "1", "2"], font=("Arial", 10)).pack(fill="x", pady=(0,10))

        # Botón calcular
        tk.Button(
            frame_principal,
            text="Recomendación",
            command=self.calcular_recomendacion,
            font=("Arial", 12, "bold"),
            bg="#2300e9",
            fg='white',
            pady=15,
            cursor="hand2"
        ).pack(fill="x", pady=30)

    def calcular_recomendacion(self):
        try:
            temperatura = float(self.temp_var.get())
            humedad = float(self.humedad_var.get())
            lluvia = float(self.lluvia_var.get())

            if not (0 <= temperatura <= 40):
                raise ValueError("La temperatura debe estar entre 0 y 40°C")
            if not (0 <= humedad <= 100):
                raise ValueError("La humedad debe estar entre 0 y 100%")
            if not (0 <= lluvia <= 2):
                raise ValueError("La lluvia debe ser 0, 1 o 2")

            if self.sistema_ctrl is None:
                raise Exception("Sistema de control no inicializado")

            sistema_sim = ctrl.ControlSystemSimulation(self.sistema_ctrl)
            sistema_sim.input['temperatura'] = temperatura
            sistema_sim.input['humedad'] = humedad
            sistema_sim.input['lluvia'] = lluvia
            sistema_sim.compute()
            resultado = sistema_sim.output['vestimenta']

            datos_entrada = {'temperatura': temperatura, 'humedad': humedad, 'lluvia': lluvia}
            VentanaResultadosDifuso(self.root, datos_entrada, resultado)

        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error del Sistema", str(e))

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    try:
        sistema = SistemaLogicaDifusa()
        sistema.ejecutar()
    except Exception as e:
        print(f"Error crítico al iniciar: {e}")
