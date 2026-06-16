# ZYZZ LEGACY

Sistema de gerenciamento de treinos desenvolvido em Python para a disciplina **Development With Python**.

## Sobre o projeto

O ZYZZ LEGACY permite registrar exercícios, séries, repetições e peso utilizado. Os dados são armazenados em um arquivo JSON para que o usuário possa consultar o histórico de treinos posteriormente.

O projeto possui duas versões:

- **Versão em terminal:** executada pelo arquivo `main.py`.
- **Versão com interface gráfica:** executada pelo arquivo `gui_main.py` e desenvolvida com Tkinter.

## Funcionalidades

- Cadastro de exercícios realizados;
- Registro de séries, repetições e peso;
- Armazenamento dos dados em JSON;
- Consulta do histórico de treinos;
- Cálculo do total de repetições;
- Sugestões de exercícios por grupo muscular;
- Validação dos dados informados;
- Interface gráfica com menu e telas de navegação.

## Tecnologias utilizadas

- Python 3;
- Tkinter;
- JSON;
- Módulo `datetime`;
- Módulo `os`.

O projeto utiliza apenas bibliotecas que fazem parte da instalação padrão do Python. Portanto, não é necessário instalar dependências externas.

## Estrutura do projeto

```text
zyzz-legacy/
├── main.py          # Versão executada no terminal
├── gui_main.py      # Versão com interface gráfica
├── .gitignore       # Arquivos ignorados pelo Git
└── README.md        # Documentação do projeto
```

O arquivo `treinos.json` é criado automaticamente após o primeiro treino ser salvo.

## Como executar

### Requisitos

- Python 3 instalado no computador.

### Interface gráfica

```bash
python gui_main.py
```

### Versão pelo terminal

```bash
python main.py
```

Em alguns computadores, use `python3` no lugar de `python`.

## Como usar

1. Abra o programa;
2. Escolha a opção **Adicionar Treino**;
3. Informe o exercício, as séries, as repetições e, opcionalmente, o peso;
4. Salve o registro;
5. Acesse **Ver Todos os Treinos** para consultar o histórico;
6. Use **Possíveis Treinos** para visualizar exercícios recomendados por grupo muscular.

## Armazenamento dos dados

Os registros são salvos localmente no arquivo `treinos.json`. Esse arquivo não é enviado ao GitHub, pois contém dados gerados durante o uso do sistema.

## Possíveis melhorias

- Edição e exclusão de registros;
- Gráficos de evolução;
- Cadastro de usuários;
- Filtros por data e exercício;
- Desenvolvimento de uma versão web.
