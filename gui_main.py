import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

ARQUIVO_TREINOS = "treinos.json"

EXERCICIOS = {
    "Peitoral": ["Supino Reto", "Supino Inclinado", "Crossover", "Crucifixo"],
    "Costas": ["Barra Fixa", "Remada Curvada", "Puxada Frontal", "Face Pull"],
    "Braço": ["Rosca Direta", "Rosca Martelo", "Tríceps Pulley", "Tríceps Corda"],
    "Quadríceps": ["Agachamento Livre", "Leg Press", "Cadeira Extensora", "Afundo"],
    "Posterior": ["Mesa Flexora", "Stiff", "Cadeira Flexora", "Flexão Nórdica"],
    "Glúteo": ["Hip Thrust", "Elevação Pélvica", "Glúteo na Polia", "Abdução"],
    "Panturrilha": ["Gêmeos em Pé", "Gêmeos Sentado", "Gêmeos no Leg Press"],
    "Abdômen": ["Prancha", "Crunch", "Elevação de Pernas", "Russian Twist"],
}


def carregar_dados():
    if not os.path.exists(ARQUIVO_TREINOS):
        return {}
    try:
        with open(ARQUIVO_TREINOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (OSError, json.JSONDecodeError):
        return {}


def salvar_dados(dados):
    with open(ARQUIVO_TREINOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


class TrainingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZYZZ LEGACY")
        self.root.geometry("900x620")
        self.root.configure(bg="#0D1117")
        self.menu()

    def limpar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def titulo(self, texto):
        tk.Label(
            self.root,
            text=texto,
            font=("Segoe UI", 24, "bold"),
            bg="#21262D",
            fg="#58A6FF",
            pady=22,
        ).pack(fill="x")

    def botao(self, texto, comando):
        ttk.Button(self.root, text=texto, command=comando).pack(fill="x", padx=140, pady=10, ipady=10)

    def menu(self):
        self.limpar()
        self.titulo("ZYZZ LEGACY")
        tk.Label(
            self.root,
            text="Construa seu legado. Rep a rep.",
            font=("Segoe UI", 11),
            bg="#0D1117",
            fg="#8B949E",
        ).pack(pady=18)
        self.botao("Adicionar Treino", self.adicionar)
        self.botao("Ver Todos os Treinos", self.historico)
        self.botao("Possíveis Treinos", self.grupos)
        self.botao("Sair", self.root.destroy)

    def adicionar(self):
        self.limpar()
        self.titulo("Adicionar Treino")
        frame = tk.Frame(self.root, bg="#161B22")
        frame.pack(fill="x", padx=100, pady=30)

        campos = {}
        for nome in ["Exercício", "Séries", "Repetições", "Peso (kg) - opcional"]:
            tk.Label(frame, text=nome, bg="#161B22", fg="#E6EDF3").pack(anchor="w", padx=25, pady=(12, 3))
            entrada = ttk.Entry(frame)
            entrada.pack(fill="x", padx=25)
            campos[nome] = entrada

        def salvar():
            exercicio = campos["Exercício"].get().strip()
            try:
                series = int(campos["Séries"].get())
                repeticoes = int(campos["Repetições"].get())
                peso_txt = campos["Peso (kg) - opcional"].get().strip()
                peso = float(peso_txt) if peso_txt else None
            except ValueError:
                messagebox.showerror("Erro", "Use números válidos para séries, repetições e peso.")
                return

            if not exercicio or series <= 0 or repeticoes <= 0:
                messagebox.showerror("Erro", "Preencha corretamente os campos obrigatórios.")
                return

            dados = carregar_dados()
            dados.setdefault(exercicio, [])
            registro = {
                "series": series,
                "repeticoes": repeticoes,
                "total": series * repeticoes,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
            if peso is not None:
                registro["peso_kg"] = peso
            dados[exercicio].append(registro)
            salvar_dados(dados)
            messagebox.showinfo("Sucesso", "Treino salvo com sucesso!")
            self.menu()

        ttk.Button(frame, text="Salvar", command=salvar).pack(side="left", padx=25, pady=25)
        ttk.Button(frame, text="Voltar", command=self.menu).pack(side="left", pady=25)

    def historico(self):
        self.limpar()
        self.titulo("Histórico de Treinos")
        texto = scrolledtext.ScrolledText(self.root, font=("Consolas", 10), bg="#161B22", fg="#E6EDF3")
        texto.pack(fill="both", expand=True, padx=30, pady=20)
        dados = carregar_dados()

        if not dados:
            texto.insert(tk.END, "Nenhum treino registrado ainda.")
        else:
            total_geral = 0
            for exercicio, registros in dados.items():
                texto.insert(tk.END, f"\n{exercicio.upper()}\n")
                texto.insert(tk.END, "-" * 60 + "\n")
                for i, registro in enumerate(registros, 1):
                    total = registro.get("total", registro["series"] * registro["repeticoes"])
                    peso = f" | {registro['peso_kg']} kg" if "peso_kg" in registro else ""
                    texto.insert(
                        tk.END,
                        f"{i}. {registro['series']}x{registro['repeticoes']} = {total} reps | {registro['data']}{peso}\n",
                    )
                    total_geral += total
            texto.insert(tk.END, f"\nTOTAL GERAL: {total_geral} repetições")

        texto.config(state="disabled")
        ttk.Button(self.root, text="Voltar", command=self.menu).pack(pady=(0, 15))

    def grupos(self):
        self.limpar()
        self.titulo("Possíveis Treinos")
        frame = tk.Frame(self.root, bg="#0D1117")
        frame.pack(fill="both", expand=True, padx=60, pady=25)

        for indice, grupo in enumerate(EXERCICIOS):
            botao = ttk.Button(frame, text=grupo, command=lambda g=grupo: self.exercicios(g))
            botao.grid(row=indice // 4, column=indice % 4, padx=10, pady=10, ipadx=15, ipady=15, sticky="nsew")
            frame.columnconfigure(indice % 4, weight=1)

        ttk.Button(self.root, text="Voltar", command=self.menu).pack(pady=15)

    def exercicios(self, grupo):
        self.limpar()
        self.titulo(grupo)
        lista = tk.Listbox(self.root, font=("Segoe UI", 13), bg="#161B22", fg="#E6EDF3")
        lista.pack(fill="both", expand=True, padx=80, pady=30)
        for indice, exercicio in enumerate(EXERCICIOS[grupo], 1):
            lista.insert(tk.END, f"{indice}. {exercicio}")
        ttk.Button(self.root, text="Voltar aos grupos", command=self.grupos).pack(pady=15)


if __name__ == "__main__":
    janela = tk.Tk()
    app = TrainingApp(janela)
    janela.mainloop()
