
# Relógio Flutuante (Overlay) para Desktop

Um widget de relógio e contador de FPS para Windows, customizável e sempre visível, ideal para gamers e multitarefas. Desenvolvido em Python, este overlay leve permite que você veja informações essenciais sem sair da sua aplicação de tela cheia.

---

## 🚀 Funcionalidades

- **Sempre Visível:** A janela permanece por cima de todas as outras, incluindo jogos em tela cheia (especialmente no modo "Janela sem Bordas").
- **Totalmente Manipulável:**
  - Mova a janela para qualquer lugar da tela.
  - Redimensione a janela clicando e arrastando suas bordas e cantos.
- **Contador de FPS:**
  - Ative um contador de FPS em tempo real com um clique.
  - O contador aparece elegantemente ao lado da hora.
  - Utiliza um método de cálculo preciso e com baixo impacto na performance.
- **Customização Visual:**
  - Alterne entre 3 níveis de transparência para uma integração perfeita com sua tela.
- **Controles Intuitivos:**
  - **`FPS`**: Liga/desliga a exibição do contador de FPS.
  - **`💧`**: Alterna os níveis de transparência.
  - **`📌`**: Fixa ou desafixa o overlay (ativa/desativa o modo "sempre visível").
  - **`×`**: Fecha o aplicativo.
  - **`Esc`**: Tecla de atalho para fechar o aplicativo.

---

## 🛠️ Como Usar

Siga os passos abaixo para configurar e executar o relógio em qualquer computador com Windows.

### Pré-requisitos

- **Python 3:** Certifique-se de que o Python está instalado. Se não estiver, baixe-o em [python.org](https://python.org/).
  - **Importante:** Durante a instalação, marque a caixa **"Add Python to PATH"**.

### Instalação

1.  **Faça o download do código:** Baixe o arquivo `relogio.overlay.pyw` deste repositório.

2.  **Abra o Prompt de Comando (CMD):** Pressione `Win + R`, digite `cmd` e aperte Enter.

3.  **Instale as dependências:** Cole o seguinte comando no CMD e pressione Enter:
    ```bash
    pip install mss numpy pywin32
    ```

### Execução

Após a instalação das dependências, basta dar um **duplo-clique** no arquivo `relogio.overlay.pyw`.

O relógio aparecerá no canto superior esquerdo da tela, pronto para ser usado!

> **Dica:** A extensão `.pyw` é usada para que o script execute sem abrir uma janela de console preta em segundo plano.

---

## 🔧 Tecnologias Utilizadas

Este projeto foi construído com as seguintes tecnologias e bibliotecas:

- **[Python 3](https://www.python.org/)**: Linguagem principal do projeto.
- **[Tkinter](https://docs.python.org/3/library/tkinter.html)**: Para a criação da interface gráfica (GUI).
- **[PyWin32](https://pypi.org/project/pywin32/)**: Para a integração com a API do Windows, permitindo o controle avançado da janela (como o modo "sempre visível").
- **[MSS](https://pypi.org/project/mss/)**: Para a captura de tela de alta velocidade e baixo custo, utilizada no contador de FPS.
- **[NumPy](https://numpy.org/)**: Para o cálculo rápido e eficiente da média de quadros por segundo.

---

## 📄 Licença

Distribuído sob a Licença MIT. Veja o arquivo `LICENSE` para mais informações.
