# ============================================
# IMPORTAÇÕES
# ============================================

import json
import os
from datetime import datetime

# ============================================
# CONSTANTES
# ============================================

ARQUIVO_TREINOS = "treinos.json"

# ============================================
# BANCO DE EXERCÍCIOS POR GRUPO MUSCULAR
# ============================================

EXERCICIOS_POR_GRUPO = {
    "1": {
        "nome": "Peitoral",
        "exercicios": [
            ("Supino Reto com Barra",        "4x8-12",  "Base para massa no peitoral médio"),
            ("Supino Inclinado com Halteres", "3x10-12", "Foco no peitoral superior"),
            ("Supino Declinado",              "3x10-12", "Ativa o peitoral inferior"),
            ("Crossover na Polia",            "3x12-15", "Isolamento com tensão constante"),
            ("Crucifixo com Halteres",        "3x12-15", "Estiramento e contração do peitoral"),
            ("Peck Deck (Fly Machine)",       "3x12-15", "Isolamento total do peitoral"),
            ("Flexão de Braço",               "3x falha", "Exercício básico e eficaz"),
            ("Supino com Halteres",           "4x10-12", "Maior amplitude de movimento"),
            ("Mergulho entre Bancos",         "3x12-15", "Peitoral inferior e tríceps"),
        ]
    },
    "2": {
        "nome": "Costas",
        "exercicios": [
            ("Barra Fixa (Pull-up)",          "4x falha", "Rei dos exercícios de costas"),
            ("Remada Curvada com Barra",      "4x8-10",  "Espessura total do dorsal"),
            ("Puxada Frontal",                "4x10-12", "Largura do dorsal"),
            ("Remada Unilateral com Haltere", "3x10-12", "Corrige desequilíbrios"),
            ("Serrote com Haltere",           "3x10-12", "Foco no grande dorsal"),
            ("Remada na Máquina",             "3x12-15", "Controle total da execução"),
            ("Pullover com Halter",           "3x12-15", "Amplia a caixa torácica"),
            ("Face Pull",                     "3x15-20", "Saúde do manguito rotador"),
            ("Remada T-Bar",                  "4x8-10",  "Espessura e força do meio das costas"),
        ]
    },
    "3": {
        "nome": "Braço",
        "exercicios": [
            ("Rosca Direta com Barra",        "3x10-12", "Bíceps — exercício base"),
            ("Rosca Alternada com Halteres",  "3x10-12", "Pico do bíceps"),
            ("Rosca Martelo",                 "3x10-12", "Braquial e bíceps longo"),
            ("Rosca Concentrada",             "3x12-15", "Isolamento máximo do bíceps"),
            ("Tríceps Testa (Skull Crusher)", "3x10-12", "Cabeça longa do tríceps"),
            ("Tríceps Pulley",                "3x12-15", "Isolamento com boa execução"),
            ("Tríceps Corda",                 "3x12-15", "Abre os feixes do tríceps"),
            ("Mergulho (Dips)",               "3x falha", "Tríceps e peitoral inferior"),
            ("Rosca 21",                      "3x21",    "Técnica avançada para bíceps"),
            ("Tríceps Francês",               "3x10-12", "Cabeça longa com haltere"),
        ]
    },
    "4": {
        "nome": "Quadríceps",
        "exercicios": [
            ("Agachamento Livre",             "4x8-12",  "Rei dos exercícios de pernas"),
            ("Leg Press 45°",                 "4x10-15", "Volume e força no quadríceps"),
            ("Extensora",                     "3x12-15", "Isolamento total do quadríceps"),
            ("Agachamento Hack",              "3x10-12", "Foco no vasto lateral"),
            ("Afundo (Lunges)",               "3x12 cada", "Equilíbrio e unilateral"),
            ("Agachamento Búlgaro",           "3x10 cada", "Força e equilíbrio"),
            ("Agachamento Sumô",              "4x10-12", "Quadríceps e adutores"),
            ("Cadeira Extensora",             "3x15-20", "Pré-exaustão do quadríceps"),
            ("Step-Up com Halteres",          "3x12 cada", "Funcional e unilateral"),
        ]
    },
    "5": {
        "nome": "Posterior",
        "exercicios": [
            ("Levantamento Terra",            "4x5-8",   "Força total de cadeia posterior"),
            ("Mesa Flexora",                  "3x10-12", "Isolamento dos isquiotibiais"),
            ("Stiff (RDL)",                   "4x10-12", "Isquio e glúteo com tensão"),
            ("Cadeira Flexora",               "3x12-15", "Isolamento sentado"),
            ("Curl Deitado",                  "3x12-15", "Isquiotibiais com peso livre"),
            ("Good Morning",                  "3x10-12", "Lombar e cadeia posterior"),
            ("Levantamento Terra Romeno",     "4x8-10",  "Versão controlada do terra"),
            ("Flexão Nórdica",                "3x falha", "Força excêntrica dos isquios"),
        ]
    },
    "6": {
        "nome": "Glúteo",
        "exercicios": [
            ("Hip Thrust com Barra",          "4x10-15", "Melhor exercício para glúteo"),
            ("Glúteo na Polia (Kickback)",    "3x15-20", "Isolamento com tensão constante"),
            ("Agachamento Sumô",              "4x10-12", "Glúteo e adutores"),
            ("Elevação Pélvica",              "3x15-20", "Base do hip thrust"),
            ("Afundo Reverso",                "3x12 cada", "Glúteo e quadríceps"),
            ("Abdução de Quadril",            "3x15-20", "Glúteo médio e mínimo"),
            ("Step-Up",                       "3x12 cada", "Funcional e glúteo"),
            ("Agachamento Búlgaro",           "3x10 cada", "Glúteo e unilateral"),
            ("Monster Walk com Elástico",     "3x15 cada", "Ativação do glúteo médio"),
        ]
    },
    "7": {
        "nome": "Panturrilha",
        "exercicios": [
            ("Gêmeos em Pé (Calf Raise)",    "4x15-20", "Gastrocnêmio — volume total"),
            ("Gêmeos Sentado",               "4x15-20", "Sóleo — parte baixa da panturrilha"),
            ("Gêmeos no Leg Press",          "3x15-20", "Segurança e amplitude"),
            ("Salto com Corda",              "3x2min",  "Condicionamento e panturrilha"),
            ("Gêmeos Unilateral",            "3x15 cada", "Corrige desequilíbrios"),
            ("Gêmeos com Haltere",           "3x20",    "Versão livre do exercício"),
            ("Dorsiflexão com Elástico",     "3x20",    "Tibial anterior — equilíbrio"),
        ]
    },
    "8": {
        "nome": "Abdômen",
        "exercicios": [
            ("Prancha (Plank)",              "3x30-60s", "Força isométrica do core"),
            ("Abdominal Crunch",             "3x20-25", "Reto abdominal superior"),
            ("Elevação de Pernas",           "3x15-20", "Reto abdominal inferior"),
            ("Russian Twist",                "3x20",    "Oblíquos e rotação"),
            ("Ab Wheel (Roda Abdominal)",    "3x10-15", "Core completo e intenso"),
            ("Vacuum Abdominal",             "3x30s",   "Transverso do abdômen"),
            ("Dragon Flag",                  "3x falha", "Exercício avançado de core"),
            ("Crunch na Polia",              "3x15-20", "Tensão constante no abdômen"),
            ("Bicicleta Abdominal",          "3x20",    "Oblíquos e coordenação"),
            ("Dead Bug",                     "3x10 cada", "Estabilidade do core"),
        ]
    },
}

# ============================================
# SEÇÃO 1: CLASSES
# ============================================

class Exercicio:
    """Representa um exercício com nome, grupo muscular, séries e repetições."""

    def __init__(self, nome: str, grupo_muscular: str, series: int, repeticoes):
        self.nome = nome
        self.grupo_muscular = grupo_muscular
        self.series = series
        self.repeticoes = repeticoes

    def __str__(self) -> str:
        return f"{self.nome} ({self.grupo_muscular}) — {self.series}x{self.repeticoes}"


class Treino:
    """Representa uma sessão de treino contendo vários exercícios."""

    def __init__(self, nome: str, objetivo: str):
        self.nome = nome
        self.objetivo = objetivo
        self.exercicios = []
        self.data = datetime.now().strftime("%d/%m/%Y %H:%M")

    def adicionar_exercicio(self, exercicio: Exercicio) -> None:
        """Adiciona um exercício à sessão."""
        self.exercicios.append(exercicio)

    def listar_exercicios(self) -> None:
        """Imprime todos os exercícios da sessão formatados."""
        print(f"\n{'='*50}")
        print(f"  📋 TREINO : {self.nome}")
        print(f"  Objetivo  : {self.objetivo}")
        print(f"  Data      : {self.data}")
        print(f"{'='*50}")
        for i, ex in enumerate(self.exercicios, 1):
            print(f"  {i:>2}. {ex}")
        print()

# ============================================
# SEÇÃO 2: FUNÇÕES DE ARQUIVO
# ============================================

def carregar_dados(arquivo: str) -> dict:
    """Carrega e retorna os dados do arquivo JSON."""
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def salvar_dados(arquivo: str, dados: dict) -> None:
    """Serializa e salva o dicionário de dados em JSON."""
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

# ============================================
# SEÇÃO 3: FUNÇÕES PRINCIPAIS
# ============================================

def adicionar_treino() -> None:
    """Solicita dados ao usuário e registra um novo treino no JSON."""
    print("\n" + "="*50)
    print("  ➕  ADICIONAR TREINO")
    print("="*50)

    try:
        exercicio = input("  Exercício : ").strip()
        if not exercicio:
            print("  ❌ Nome do exercício não pode ser vazio.\n")
            return

        series = int(input("  Séries    : "))
        reps = int(input("  Repetições: "))

        if series <= 0 or reps <= 0:
            print("  ❌ Séries e repetições precisam ser maiores que zero.\n")
            return

        peso_raw = input("  Peso (kg) — deixe vazio se não usar: ").strip()
        peso = float(peso_raw) if peso_raw else None

    except ValueError:
        print("  ❌ Séries e repetições precisam ser números inteiros.\n")
        return

    treinos = carregar_dados(ARQUIVO_TREINOS)
    if exercicio not in treinos:
        treinos[exercicio] = []

    registro = {
        "series": series,
        "repeticoes": reps,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "total": series * reps,
    }
    if peso is not None:
        registro["peso_kg"] = peso

    treinos[exercicio].append(registro)
    salvar_dados(ARQUIVO_TREINOS, treinos)

    peso_txt = f"{peso} kg" if peso else "—"
    print("\n  ✅ Treino salvo!")
    print(f"     {exercicio}  ·  {series}x{reps}  ·  Peso: {peso_txt}")
    print(f"     Total: {series * reps} repetições\n")


def ver_todos_treinos() -> None:
    """Exibe o histórico completo de treinos registrados."""
    print("\n" + "="*50)
    print("  📋  HISTÓRICO DE TREINOS")
    print("="*50)

    treinos = carregar_dados(ARQUIVO_TREINOS)

    if not treinos:
        print("  Nenhum treino registrado ainda. Comece agora! 💪\n")
        return

    total_geral = 0

    for exercicio, registros in treinos.items():
        print(f"\n  🏋️  {exercicio.upper()}")
        print("  " + "─" * 46)

        total_exercicio = 0
        for i, r in enumerate(registros, 1):
            peso_str = f"  ·  {r['peso_kg']} kg" if "peso_kg" in r else ""
            total = r.get("total", r["repeticoes"] * r["series"])
            print(f"    {i:>2}. {r['repeticoes']}x{r['series']}  "
                  f"= {total} reps  ·  {r['data']}{peso_str}")
            total_exercicio += total

        print(f"        Subtotal: {total_exercicio} repetições")
        total_geral += total_exercicio

    print("\n" + "="*50)
    print(f"  TOTAL GERAL: {total_geral:,} repetições")
    print("="*50 + "\n")


def possíveis_treinos() -> None:
    """Exibe o menu de grupos musculares e lista os exercícios do grupo escolhido."""

    while True:
        print("\n" + "="*50)
        print("  🏆  POSSÍVEIS TREINOS")
        print("="*50)
        print("  Escolha um grupo muscular:\n")

        for key, info in EXERCICIOS_POR_GRUPO.items():
            qtd = len(info["exercicios"])
            print(f"    {key}. {info['nome']:<14}  ({qtd} exercícios)")

        print("\n    0. ← Voltar ao menu principal")
        print("="*50)

        opcao = input("  Opção: ").strip()

        if opcao == "0":
            return

        if opcao not in EXERCICIOS_POR_GRUPO:
            print("  ❌ Opção inválida. Tente novamente.\n")
            continue

        grupo = EXERCICIOS_POR_GRUPO[opcao]
        nome = grupo["nome"]
        exercicios = grupo["exercicios"]

        print(f"\n{'='*50}")
        print(f"  🏋️  {nome.upper()}")
        print(f"  {len(exercicios)} exercícios recomendados")
        print("="*50)
        print(f"  {'#':<4}  {'Exercício':<34}  {'Série Rec.':<12}  Descrição")
        print("  " + "─" * 80)

        for i, (nome_ex, series_rec, desc) in enumerate(exercicios, 1):
            print(f"  {i:<4}  {nome_ex:<34}  {series_rec:<12}  {desc}")

        print("="*50)
        input("\n  Pressione Enter para voltar aos grupos...")

# ============================================
# SEÇÃO 4: MENU PRINCIPAL
# ============================================

def menu() -> None:
    """Loop principal que exibe o menu e roteia as opções do usuário."""
    while True:
        print("\n" + "="*50)
        print("       💀  ZYZZ LEGACY  💀")
        print("  Construa seu legado. Rep a rep.")
        print("="*50)
        print("  1. ➕  Adicionar Treino")
        print("  2. 📋  Ver Todos os Treinos")
        print("  3. 🏆  Possíveis Treinos")
        print("  4. 🚪  Sair")
        print("="*50)

        opcao = input("  Escolha: ").strip()

        if opcao == "1":
            adicionar_treino()
        elif opcao == "2":
            ver_todos_treinos()
        elif opcao == "3":
            possíveis_treinos()
        elif opcao == "4":
            print("\n  Até logo! Continue o legado! 💪\n")
            break
        else:
            print("  ❌ Opção inválida. Digite 1, 2, 3 ou 4.\n")

# ============================================
# PONTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    menu()
