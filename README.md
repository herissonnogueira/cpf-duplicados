# Verificação de CPFs Duplicados em XML de Prestação de Contas

Este script automatiza a verificação de CPFs duplicados em arquivos XML grandes, com mais de 100 mil linhas, gerando relatórios em **PDF** (mais utilizado) e **.txt** (para testes).

## Tecnologias

- **Python** com:
  - `xml.etree.ElementTree`: Para leitura e manipulação de XML.
  - `collections`: Para manipulação de dados.
  - `fpdf`: Para criação de relatórios em PDF.

## Funcionalidades

- **Verificação de XML**: Percorre as principais tags (`edu:escola`, `edu:turma`, `edu:aluno`, etc.) para encontrar CPFs duplicados.
- **Relatórios**: Gera saídas em **PDF** e **.txt**.

## Como Usar

### Pré-requisitos

- **Python** instalado.

### Passos

1. Clone o repositório:
    ```bash
    git clone https://github.com/herissonnogueira/cpf-duplicados.git
    ```

2. Navegue até a pasta do script:
    ```bash
    cd cpf-duplicados
    ```

3. Instale as dependências:
     ```bash
     pip install fpdf
     ```

4. Coloque o arquivo XML na pasta do projeto (nome padrão: `Educacao.xml`):
    ```
    /cpf-duplicados
    │
    ├── main.py
    ├── Educacao.xsd
    └── Educacao.xml
    ```

5. Execute o script:
    ```bash
    python main.py
    ```

6. Saída:
  - `cpfs_duplicados.txt` (para testes).
  - `cpfs_duplicados.pdf` (relatório principal).

### Ajustes para XMLs de 2024

Para arquivos XML de 2024, ajuste o **namespace** no código e adicione as novas modalidades de verificação.

### Exemplo de Relatório

O relatório gerado inclui:
- CPF duplicado.
- ID e Nome da Escola.
- Nome da turma e do aluno.

Se tiver alguma dúvida, fique à vontade para entrar em contato comigo:

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/herissonnogueira/)
