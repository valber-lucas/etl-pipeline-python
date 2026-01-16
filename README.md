# 🚀 High-Performance ETL Pipeline (Python)

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

### Fluxo de Dados
```mermaid
graph LR
    A[CSV File] -->|Stream| B(Generator Python)
    B -->|Yield| C{Transform}
    C -->|Invalid| D[Log Error]
    C -->|Valid| E[Batch Buffer]
    E -->|Full?| F[(SQLite DB)]
    
    style A fill:#f9f,stroke:#333
    style F fill:#bbf,stroke:#333
```
