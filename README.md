# Technical Test Stract

API REST em Python/Flask para geração de relatórios de anúncios de diferentes plataformas.

## Requisitos

- Python 3.12+
- Poetry

## Instalação

1. Instale o Python 3.12+ de acordo com seu sistema operacional em [python.org](https://python.org)

2. Instale o Poetry:
   ```bash
   # Windows (PowerShell)
   (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

   # Linux/MacOS
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Configure o projeto:
   ```bash
   # Clone o repositório
   git clone https://github.com/seu-usuario/technical-test-stract.git
   cd technical-test-stract

   # Configure variáveis de ambiente para autenticação dos endpoints.

   # Instale dependências
   poetry install
   ```

## Uso

```bash
# Ative o ambiente virtual
poetry shell

# Execute a aplicação
python app.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints

- `GET /`: Informações do autor
- `GET /<platform>`: Anúncios de uma plataforma
- `GET /<platform>/resumo`: Resumo por conta
- `GET /geral`: Todos os anúncios
- `GET /geral/resumo`: Resumo por plataforma