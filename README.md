# High-Performance ETL Pipeline (Python)

Pipeline de Engenharia de Dados capaz de processar e ingerir datasets massivos com consumo de memória constante (O(1)).

## ⚡ Performance Benchmark
- **Dataset:** 1 Milhão de registros (CSV gerado sinteticamente).
- **Tempo de Processamento:** ~2.4 segundos.
- **Estratégia:** Generators (Streaming) + Batch Insert (SQL).

## 🛠️ Tecnologias
- **Python 3.12+**
- **SQLite** (Persistência Relacional)
- **Logging** (Rastreabilidade Enterprise)
- **CI/CD:** GitHub Actions (Automated Testing)

## ⚙️ Arquitetura
O projeto resolve o problema de "Memory Overflow" ao ler arquivos maiores que a RAM disponível:

1.  **Extract:** Leitura via `yield` (Lazy Loading).
2.  **Transform:** Normalização e validação de tipos com `Type Hints`.
3.  **Load:** Inserção em lotes (Batch Size: 5000) para otimizar I/O.

## Como Rodar o Projeto

Gere o dataset de teste:

Bash
python generate_data.py

Execute o pipeline:

Bash
python etl_processor.py

Rode os testes unitários:

Bash
python test_etl.py

### Fluxo de Dados
```mermaid
graph LR
    A[📄 CSV File<br>1M+ Rows] -->|Stream Lazy Loading| B(⚙️ Generator Python)
    B -->|Yield Row| C{🔍 Transform & Validate}
    C -->|Invalid| D[🗑️ Discard/Log]
    C -->|Valid| E[📦 Batch Buffer]
    E -->|Batch Full?| F[(🗄️ SQLite Database)]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px

## Como Rodar o Projeto
Gere o dataset de teste:

Bash

python generate_data.py
Execute o pipeline:

Bash

python etl_processor.py
Rode os testes unitários:

Bash

python test_etl.py