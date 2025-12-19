# Validador de Documentos Empresariais

Sistema de validação automatizada de documentos empresariais brasileiros (Contrato Social, Cartão CNPJ e Certidão Negativa de Débitos Federais) utilizando LLM para extração estruturada de dados e validação semântica de objeto social, combinado com validações determinísticas para garantir consistência entre documentos.

## 📁 Estrutura do Projeto

### `/app`
Diretório principal da aplicação.

- **`main.py`**: Ponto de entrada da aplicação FastAPI, configuração de rotas e handlers de exceção.
- **`api/`**: Camada de API REST
  - **`v1/routers/validation.py`**: Endpoint de validação de documentos
  - **`v1/schemas.py`**: Modelos Pydantic para requisições e respostas da API
  - **`error_handlers.py`**: Tratamento centralizado de exceções
- **`core/`**: Configurações e utilitários centrais
  - **`config.py`**: Configurações da aplicação (LLM, logging, etc.)
  - **`exceptions.py`**: Exceções customizadas do domínio
  - **`logging.py`**: Configuração de logging estruturado
  - **`utils/normalization.py`**: Funções de normalização de texto
- **`domain/`**: Lógica de negócio e validações
  - **`models.py`**: Modelos de domínio (Contrato Social, CNPJ, Certidão)
  - **`document_validator.py`**: Orquestrador de validações
  - **`validators/`**: Validadores específicos por campo
    - `cnpj.py`: Validação de consistência de CNPJ
    - `company_name.py`: Validação de razão social
    - `legal_nature.py`: Validação de natureza jurídica
    - `address.py`: Validação de endereço
    - `partners.py`: Validação de sócios/QSA
    - `tax_status.py`: Validação de situação cadastral
    - `expiration.py`: Validação de validade de certidão
    - `business_purpose.py`: Validação de objeto social vs atividades CNAE (usa LLM)
- **`services/`**: Serviços de infraestrutura
  - **`text_extractor.py`**: Extração de texto de PDFs usando PyPDF
  - **`structured_extractor.py`**: Extração estruturada usando LLM (chama prompts e valida JSON)
  - **`llm_client.py`**: Cliente para comunicação com OpenRouter API
  - **`prompts.py`**: Templates de prompts para LLM
  - **`validation_use_case.py`**: Caso de uso principal que orquestra todo o fluxo

## 🔄 Processo de Validação

O sistema segue um fluxo bem definido em 4 etapas principais:

### 1. Extração de Texto dos PDFs
- Utiliza a biblioteca **PyPDF** para extrair texto bruto dos arquivos PDF
- Processa três documentos em paralelo:
  - Contrato Social
  - Cartão CNPJ
  - Certidão Negativa de Débitos Federais

### 2. Extração Estruturada com LLM
- O texto extraído é enviado para um **LLM (Large Language Model)** via OpenRouter
- O LLM recebe prompts específicos para cada tipo de documento
- O LLM retorna um **JSON estruturado** com os dados extraídos
- O JSON é validado contra modelos Pydantic para garantir estrutura correta

### 3. Validação de Inconsistências
- Após a extração, o sistema executa uma série de **validadores determinísticos**:
  - Consistência de CNPJ entre documentos
  - Consistência de razão social
  - Consistência de natureza jurídica
  - Consistência de endereço
  - Validação de situação cadastral
  - Validação de validade da certidão
  - Consistência de sócios/QSA

### 4. Validação de Objeto Social (com LLM)
- Para o objeto social, utiliza-se **LLM novamente** para validação semântica
- Compara o objeto social do Contrato Social com as atividades CNAE do Cartão CNPJ
- O LLM faz análise semântica para verificar se todas as atividades do CNPJ estão contempladas no objeto social
- Esta validação é mais complexa pois requer compreensão de contexto e sinônimos

## 🏗️ Decisões de Arquitetura

### Uso do LLM: Extração e Validação Semântica

O LLM é utilizado em **duas etapas distintas** do processo:

1. **Extração Estruturada**: O LLM extrai dados estruturados dos documentos PDFs, convertendo texto não estruturado em JSON validado
2. **Validação Semântica de Objeto Social**: O LLM realiza análise semântica para verificar se as atividades CNAE estão contempladas no objeto social

### Por que Validações Determinísticas para a Maioria dos Campos?

A decisão de usar validações determinísticas em código para a maioria dos campos foi tomada por várias razões:

1. **Confiabilidade**: Validações determinísticas são mais confiáveis e previsíveis
2. **Performance**: Validações em código são muito mais rápidas que chamadas a LLM
3. **Custo**: Reduzir chamadas a LLM diminui custos operacionais
4. **Rastreabilidade**: Validações em código são mais fáceis de debugar e auditar
5. **Manutenibilidade**: Regras de negócio em código são mais fáceis de manter e evoluir

### Por que LLM para Validação de Objeto Social?

A validação de objeto social é uma exceção justificada porque:

1. **Complexidade Semântica**: Requer compreensão de sinônimos e contexto (ex: "Desenvolvimento de software" vs "Consultoria em Tecnologia")
2. **Variabilidade Linguística**: Objetos sociais podem ser escritos de formas muito diferentes
3. **Análise Contextual**: Precisa entender se uma atividade está "contemplada" mesmo que não esteja explicitamente escrita
4. **Dificuldade de Regras Fixas**: Seria extremamente difícil criar regras determinísticas que cobrissem todos os casos

Portanto, o LLM é usado como uma ferramenta de **análise semântica** para este caso específico, enquanto todas as outras validações seguem regras determinísticas.

## 🚀 Como Iniciar o Projeto

### Pré-requisitos

- Python 3.11 ou superior
- Docker e Docker Compose (opcional, para execução via Docker)
- Conta no OpenRouter com API key (para acesso ao LLM)

### Configuração

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd valida-documentos
```

2. Crie um arquivo `.env` na raiz do projeto:
```env
OPENROUTER_API_KEY=sua_api_key_aqui
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_MODEL=google/gemini-2.0-flash-001
OPENROUTER_TEMPERATURE=0.0
LLM_TIMEOUT_SECONDS=30
LOG_LEVEL=INFO
LOG_DIR=logs
```

### Opção 1: Execução com Docker (Recomendado)

1. Construa e inicie o container:
```bash
docker-compose up --build
```

2. A aplicação estará disponível em `http://localhost:8000`

3. Acesse a documentação interativa em `http://localhost:8000/docs`

### Opção 2: Execução Local (Sem Docker)

1. Crie um ambiente virtual:
```bash
python -m venv venv
```

2. Ative o ambiente virtual:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. A aplicação estará disponível em `http://localhost:8000`

## 📚 Documentação da API

Após iniciar a aplicação, acesse:

- **Swagger UI**: `http://localhost:8000/docs`

### Endpoint Principal

**POST** `/api/v1/validate`

Valida três documentos empresariais:
- Contrato Social (PDF)
- Cartão CNPJ (PDF)
- Certidão Negativa de Débitos Federais (PDF)

**Resposta:**

Exemplo com inconsistências:
```json
{
  "status": "REPROVADO",
  "inconsistencies": [
    {
      "field": "cnpj",
      "message": "CNPJ divergente entre documentos.",
      "severity": "CRITICA",
      "values": {
        "cartao_cnpj": "12345678000190",
        "certidao_negativa": "12345678000199"
      }
    },
    {
      "field": "razao_social",
      "message": "Razão social não confere entre contrato social e cartão CNPJ.",
      "severity": "CRITICA",
      "values": {
        "contrato_social": "empresa exemplo limitada",
        "cartao_cnpj": "empresa exemplo ltda"
      }
    },
    {
      "field": "certidao_validade",
      "message": "Certidão negativa expirada.",
      "severity": "CRITICA",
      "values": {
        "data_validade": "2024-12-01",
        "data_atual": "2025-01-15"
      }
    }
  ]
}
```

Exemplo sem inconsistências:
```json
{
  "status": "APROVADO",
  "inconsistencies": []
}
```

## 🔧 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para APIs
- **Pydantic**: Validação de dados e modelos
- **PyPDF**: Extração de texto de PDFs
- **OpenRouter**: Gateway para acesso a múltiplos modelos LLM
- **Uvicorn**: Servidor ASGI de alta performance
- **Docker**: Containerização da aplicação

## 📝 Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `OPENROUTER_API_KEY` | Chave de API do OpenRouter | **Obrigatório** |
| `OPENROUTER_BASE_URL` | URL base da API OpenRouter | `https://openrouter.ai/api/v1/chat/completions` |
| `OPENROUTER_MODEL` | Modelo LLM a ser usado | `google/gemini-2.0-flash-001` |
| `OPENROUTER_TEMPERATURE` | Temperatura do modelo (0.0 = determinístico) | `0.0` |
| `LLM_TIMEOUT_SECONDS` | Timeout para chamadas LLM | `30` |
| `LOG_LEVEL` | Nível de log | `INFO` |
| `LOG_DIR` | Diretório de logs | `logs` |

## 🧪 Testes

TODO

```bash
pytest
```

## 📊 Logging

O sistema utiliza logging estruturado. Os logs são salvos em:
- Arquivo: `logs/app.log`
- Console: Baseado no nível configurado

## 🔒 Segurança

- Arquivos `.env` não são versionados (veja `.gitignore`)
- Logs não são versionados
- API key deve ser mantida em segredo

