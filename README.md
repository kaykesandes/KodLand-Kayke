# Jogo Kodland

Bem-vindo ao **Jogo Kodland**, um jogo simples e divertido desenvolvido com **Pygame Zero**. O objetivo é controlar o herói, evitar os inimigos e sobreviver o máximo de tempo possível enquanto acumula pontos.

---

## 🎮 Como Jogar

- **Movimentação do Herói**:

  - Use as **setas direcionais** do teclado para mover o herói.
  - O herói não pode sair das bordas da tela. Ao atingir uma borda, ele para e exibe a animação de "idle" (parado).
- **Objetivo**:

  - Evite os inimigos que se movem pela tela.
  - Sobreviva o máximo de tempo possível para acumular pontos.
- **Pontuação**:

  - Você ganha **1 ponto por segundo** enquanto sobrevive.
- **Game Over**:

  - O jogo termina quando o herói colide com um inimigo.
  - A pontuação final será exibida na tela de "Game Over".

---

## 🕹️ Controles

- **Setas direcionais**: Movem o herói.
- **Enter**: Inicia o jogo ou retorna ao menu principal.
- **M**: Ativa/desativa a música.
- **ESC**: Sai do jogo ou retorna ao menu principal.

---

## ⚙️ Mecânicas do Jogo

### 1. Estados do Jogo

O jogo possui três estados principais:

- **Menu**: Tela inicial onde o jogador pode iniciar o jogo, ativar/desativar a música ou sair.
- **Jogo**: O estado principal onde o jogador controla o herói e tenta sobreviver.
- **Game Over**: Tela exibida quando o herói colide com um inimigo.

### 2. Movimentação dos Inimigos

- Os inimigos se movem aleatoriamente em quatro direções: **esquerda**, **direita**, **cima** e **baixo**.
- A cada 20 segundos, a velocidade dos inimigos dobra, tornando o jogo mais desafiador.

### 3. Aumento de Velocidade

- **Inimigos**: A velocidade dos inimigos dobra a cada 20 segundos.
- **Herói**: A velocidade do herói aumenta em 1/3 do valor atual a cada 20 segundos, mas em uma proporção menor que a dos inimigos.

### 4. Música

- O jogo possui música de fundo que pode ser ativada ou desativada pressionando a tecla **M** no menu principal.

---

## 🛠️ Como Executar o Jogo

1. Certifique-se de ter o **Python** instalado em sua máquina.
2. Instale a biblioteca **Pygame Zero** executando o comando:
   ```bash
   pip install pgzero
   ```
3. Execute o jogo com o comando:
   ```bash
   pgzrun main.py
   ```

---

## 📂 Estrutura do Projeto

```
/kodland
├── main.py          # Código principal do jogo
├── assets/          # Recursos do jogo (imagens, sons, etc.)
└── README.md        # Documentação do jogo
```

---

## 🚀 Melhorias Futuras

- Adicionar novos tipos de inimigos com comportamentos diferentes.
- Implementar power-ups para o herói, como aumento temporário de velocidade ou invencibilidade.
- Adicionar níveis ou fases com diferentes layouts e desafios.

---

## 📝 Créditos

Este jogo foi desenvolvido como parte de um projeto de aprendizado com **Pygame Zero**. Agradecimentos especiais à **Kodland** e ao desenvolvedor **Kayke Sandes**
