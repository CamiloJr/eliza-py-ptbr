# ELIZA-PY — adaptação para Português Brasileiro (PT-BR)

Esta versão adapta o projeto **eliza-py** e o script **DOCTOR**, inspirado na ELIZA de Joseph Weizenbaum, para conversação em **português brasileiro**.

A adaptação não é uma tradução literal das frases em inglês. As regras foram reescritas para preservar sentido **semântico, sintático e lexical** em PT-BR, mantendo o funcionamento clássico da ELIZA baseado em palavras-chave, decomposição, remontagem, ranking e memória.

## Requisitos

- Python 3.x
- Nenhuma biblioteca externa é necessária.

## Executar

No diretório do projeto:

```bash
python eliza.py
```

Exemplo:

```text
Eliza: Olá. Conte-me o que está acontecendo.
Você: Eu estou triste
Eliza: Sinto muito que você esteja se sentindo triste.
Você: Eu quero ajuda
Eliza: O que significaria para você conseguir ajuda?
```

Para encerrar, use `tchau`, `adeus`, `sair`, `fim`, `terminar`, `encerrar` ou `até logo`.

Para reiniciar o ciclo das respostas e limpar a memória durante uma sessão, use `reiniciar` ou `reset`.

## Arquivos linguísticos

### `scripts/general.json`

Contém as informações gerais da adaptação PT-BR:

- `substitutions`: normalização lexical e ortográfica da entrada, incluindo formas como `vc → você`, `tô → estou`, `ta → está`, `nao → não`, além de sinônimos e saudações;
- `reflections`: reflexões de pessoa e posse utilizadas **somente nos componentes remontados**, por exemplo `eu → você`, `meu → seu` e `minha → sua`;
- `tags`: campos semânticos, como família, desejo, crença, felicidade e tristeza;
- `memory_inputs`: palavras que alimentam a pilha de memória;
- `exit_inputs`: expressões utilizadas para encerrar a conversa.

### `scripts/doctor.json`

Contém o script DOCTOR adaptado para PT-BR:

- palavras-chave e seus rankings;
- regras de decomposição;
- respostas de remontagem;
- regras especiais para memória (`^`) e resposta genérica (`$`).

## Alterações no motor para português

O inglês permite reflexões simples como `I ↔ you` e `am ↔ are`. Em português, aplicar a mesma estratégia diretamente quebra concordância e flexão verbal. Por isso esta versão faz algumas alterações no motor original:

1. **Normalização e reflexão foram separadas.** A entrada é normalizada antes do reconhecimento das regras, mas a mudança de perspectiva é aplicada apenas aos fragmentos que voltam para a resposta.
2. **Palavras-chave compostas são reconhecidas.** Expressões como `por que` e `o que` podem ter ranking próprio.
3. **Substituições de expressões inteiras são suportadas.** Isso permite, por exemplo, `boa noite → olá` e reflexões como `com você → comigo`.
4. **Reflexões verbais são conservadoras.** Formas inequivocamente de primeira pessoa podem ser convertidas para a forma usada com `você`, mas formas ambíguas de terceira pessoa não são alteradas cegamente.
5. **Os JSON são abertos explicitamente como UTF-8**, garantindo acentos em Windows, Linux e macOS.

Essas alterações continuam determinísticas e baseadas em regras; não foi adicionado aprendizado de máquina, modelo de linguagem ou serviço externo.

## Testes

Há testes básicos em `tests/test_ptbr.py`. Execute:

```bash
python -m unittest discover -s tests -v
```

Eles verificam, entre outros casos:

- português coloquial (`vc`, `tá`);
- sentimentos;
- reflexões de pronomes e possessivos;
- preservação de verbos de terceira pessoa;
- palavras-chave compostas;
- perguntas sobre ajuda;
- memória;
- saudações.

## Estrutura principal

```text
eliza-py/
├── eliza.py
├── README.md
├── scripts/
│   ├── general.json          # PT-BR
│   └── doctor.json           # PT-BR
├── tests/
│   └── test_ptbr.py
└── utils/
    ├── language.py
    ├── rank.py
    ├── response.py
    ├── rules.py
    └── startup.py
```

## Referência

J. Weizenbaum, “ELIZA—a computer program for the study of natural language communication between man and machine,” *Communications of the ACM*, vol. 9, no. 1, pp. 36–45, 1966.

A base deste projeto é a implementação `eliza-py` de rdimaio. O mecanismo continua inspirado no script DOCTOR e na notação de decomposição/remontagem descrita por Weizenbaum.
