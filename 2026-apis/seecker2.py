import customtkinter as ctk
import requests
from tkinter import messagebox

# Configuración visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class SistemaSeekerV6(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Módulo de Consulta Premium - Seeker-V6")
        self.geometry("550x650")

        # --- Configuración de Conexión ---
        self.api_url = "https://seeker-v6.com/personas/apiPremium/dni"
        self.token = "TOQUEN AQUI PAPU"

        self.init_ui()

    def init_ui(self):
        self.main_container = ctk.CTkFrame(self, corner_radius=20)
        self.main_container.pack(pady=30, padx=30, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(
            self.main_container, text="SEEKER-V6 API", font=("Consolas", 26, "bold")
        )
        self.label_title.pack(pady=(20, 10))

        self.status_tag = ctk.CTkLabel(
            self.main_container,
            text="CONEXIÓN PREMIUM ACTIVA",
            text_color="#4CAF50",
            font=("Roboto", 10, "bold"),
        )
        self.status_tag.pack()

        self.dni_input = ctk.CTkEntry(
            self.main_container,
            placeholder_text="Ingrese DNI a buscar",
            height=50,
            font=("Roboto", 18),
            justify="center",
            border_color="#4CAF50",
        )
        self.dni_input.pack(pady=30, padx=40, fill="x")

        self.search_btn = ctk.CTkButton(
            self.main_container,
            text="EJECUTAR BÚSQUEDA",
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            command=self.ejecutar_consulta,
            font=("Roboto", 14, "bold"),
        )
        self.search_btn.pack(pady=10, padx=40, fill="x")

        self.display_box = ctk.CTkTextbox(
            self.main_container, font=("Consolas", 12), fg_color="#1a1a1a", border_width=1
        )
        self.display_box.pack(pady=20, padx=20, fill="both", expand=True)
        self.display_box.insert("0.0", "Esperando entrada de datos...")
        self.display_box.configure(state="disabled")

    def ejecutar_consulta(self):
        dni = self.dni_input.get().strip()

        if len(dni) != 8 or not dni.isdigit():
            messagebox.showwarning("Error de Entrada", "El DNI debe tener exactamente 8 números.")
            return

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {"dni": dni}

        self.search_btn.configure(state="disabled", text="BUSCANDO EN SEEKER...")
        self.limpiar_display()

        try:
            response = requests.post(self.api_url, headers=headers, data=payload, timeout=12)

            if response.status_code == 200:
                try:
                    resultado = response.json()
                    self.imprimir_resultado(resultado)
                except Exception:
                    self.imprimir_resultado(response.text)
            else:
                self.imprimir_resultado(
                    f"ERROR DEL SERVIDOR\nCódigo: {response.status_code}\nMensaje: {response.text}"
                )

        except Exception as e:
            messagebox.showerror("Fallo de Red", f"No se pudo conectar con Seeker-V6:\n{str(e)}")
        finally:
            self.search_btn.configure(state="normal", text="EJECUTAR BÚSQUEDA")

    def imprimir_resultado(self, data):
        self.display_box.configure(state="normal")
        self.display_box.delete("0.0", "end")

        # Caso esperado: viene {"data": {...}, "status": "...", ...}
        if isinstance(data, dict) and "data" in data:
            persona = data["data"]

            texto = (
                "🧾 RESULTADO DE LA CONSULTA\n"
                + "=" * 40 + "\n"
                f"🆔 DNI: {persona.get('dni','-')}\n"
                f"👤 NOMBRE: {persona.get('nombres','')} {persona.get('ap_paterno','')} {persona.get('ap_materno','')}\n"
                f"🎂 EDAD: {persona.get('edad','-')}\n"
                f"💍 ESTADO CIVIL: {persona.get('estado_civil','-')}\n"
                f"🏠 DIRECCIÓN: {persona.get('dirección','-')}\n"
            )

            self.display_box.insert("end", texto)

        else:
            # Cualquier otra respuesta (error, texto, etc.)
            self.display_box.insert("end", "⚠ RESPUESTA DEL SERVIDOR:\n" + str(data))

        self.display_box.configure(state="disabled")

    def limpiar_display(self):
        self.display_box.configure(state="normal")
        self.display_box.delete("0.0", "end")
        self.display_box.configure(state="disabled")


if __name__ == "__main__":
    app = SistemaSeekerV6()
    app.mainloop()

