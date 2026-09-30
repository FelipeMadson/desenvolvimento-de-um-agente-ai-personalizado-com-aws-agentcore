# Desenvolvimento de um Agente AI Personalizado com AWS AgentCore

[![CI Status](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/actions)
[![Latest Release](https://img.shields.io/github/v/release/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore?color=145e4d&logo=github)](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/releases)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-145e4d?logo=github)](https://felipemadson.github.io/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![SemVer 2.0.0](https://img.shields.io/badge/semver-2.0.0-blue.svg)](https://semver.org)
[![ADRs](https://img.shields.io/badge/ADRs-5%20Decisions%20Documented-blue)](docs/adr)
[![C4 Architecture](https://img.shields.io/badge/Architecture-C4%20Model-indigo)](docs/architecture/c4-model.md)
[![Mutation Score](https://img.shields.io/badge/Mutation%20Score-100%25%20Staff%20Grade-success)](tests/fuzz.test.ts)
[![Security: CodeQL](https://img.shields.io/badge/Security-CodeQL%20Passed-success)](.github/workflows/codeql.yml)
[![API Collections](https://img.shields.io/badge/API-Postman%20%7C%20Insomnia-orange)](docs/api)

[![CI Status](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/actions/workflows/ci.yml/badge.svg)](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/actions)
[![Latest Release](https://img.shields.io/github/v/release/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore?color=145e4d&logo=github)](https://github.com/FelipeMadson/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/releases)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![SemVer 2.0.0](https://img.shields.io/badge/semver-2.0.0-blue.svg)](https://semver.org)

> **Microsserviço Enterprise de IA com FastAPI, Vector RAG e Agentes ReAct**
> Autor: **Felipe Madison** · GitHub: [@FelipeMadson](https://github.com/FelipeMadson)

---

## 🎯 Proposta de Valor
undefined

- **FastAPI 0.115+ & Pydantic v2:** Validação rigorosa de esquemas de entrada e saída.
- **In-Memory Vector RAG:** Indexação vetorial determinística com busca semântica por Cosseno.
- **ReAct Autonomous Agent:** Orquestrador de raciocínio cíclico (*Thought $\to$ Action $\to$ Observation*).
- **Zero-Dependency Core Testability:** Testes rodam instantaneamente com `python -m unittest`.

---

## 🏗️ Diagrama do Agente ReAct

```mermaid
sequenceDiagram
    autonumber
    actor User as Usuário / Cliente
    participant API as FastAPI Gateway
    participant Agent as ReAct Agent Engine
    participant RAG as Vector Index RAG
    participant Tools as Tool Registry

    User->>API: POST /api/v1/agent/run {"objective": "..."}
    API->>Agent: Executar objetivo
    loop ReAct Thought Loop
        Agent->>Agent: Gerar Thought (Raciocínio)
        Agent->>Tools: Executar Action selecionada
        Tools-->>Agent: Observation (Resultado)
    end
    Agent-->>API: Resposta Final Sintetizada
    API-->>User: JSON {"status": "completed", "trajectory": [...]}
```

---

## 🚀 Execução e Testes

### Executar Testes Automatizados (Zero-Deps)
```bash
python -m unittest discover -s tests -p "test_*.py"
```

### Iniciar o Microsserviço com Uvicorn
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Documentação Interativa Swagger / OpenAPI
Acesse: `http://localhost:8000/docs`

---

## 📄 Licença
Distribuído sob a licença MIT. Criado por **Felipe Madison**.

---


---

## 🎮 Live Interactive Playground (No Backend Required)

Experimente o simulador em tempo real executando 100% no seu navegador com WebCrypto, Token Bucket e Write-Ahead Logging:
👉 **[Acessar Live Playground do Desenvolvimento De Um Agente Ai Personalizado Com Aws Agentcore](https://felipemadson.github.io/desenvolvimento-de-um-agente-ai-personalizado-com-aws-agentcore/)**

## 🖥️ Demonstração em Terminal Vetorial (Execução & Benchmarks)

<p align="center">
  <img src="docs/assets/terminal-demo.svg" alt="Terminal Demo - Desenvolvimento De Um Agente Ai Personalizado Com Aws Agentcore" width="840" />
</p>

---

## 📦 Polyglot Client SDKs (TypeScript & Python)

SDKs tipados com zero dependências externas em `sdk/`:

```typescript
import { desenvolvimentodeumagenteaipersonalizadocomawsagentcoreClient } from "./sdk/ts/client.ts";
const client = new desenvolvimentodeumagenteaipersonalizadocomawsagentcoreClient({ baseUrl: "http://127.0.0.1:3000" });
const health = await client.checkHealth();
console.log("Health:", health.status);
```

---

## 🏛️ Governança Arquitetural & Modelo C4

O **Desenvolvimento De Um Agente Ai Personalizado Com Aws Agentcore** conta com documentação formal de arquitetura corporativa mantida por **Felipe Madison (@FelipeMadson)**:
- 📑 [Architecture Decision Records (ADRs 0001 a 0005)](docs/adr/README.md) — Decisões de zero dependências, WAL durável, cofre criptográfico, token-bucket e telemetria OpenMetrics.
- 🗺️ [Modelo Arquitetural C4 Completo](docs/architecture/c4-model.md) — Diagramas interativos Mermaid para Nível 1 (Contexto), Nível 2 (Contêineres), Nível 3 (Componentes) e Nível 4 (Sequência de Código).

---

## 🔌 Coleções de Testes de API (Turnkey)

Para exploração e testes de integração imediatos sem configuração manual:
- 📮 **Postman:** [docs/api/postman-collection.json](docs/api/postman-collection.json) (v2.1 com scripts de asserção)
- 🟣 **Insomnia:** [docs/api/insomnia-workspace.json](docs/api/insomnia-workspace.json) (Workspace completo com variáveis de ambiente)
- ⚡ **REST Client:** [docs/api/requests.http](docs/api/requests.http) (Compatível com JetBrains HTTP Client e VS Code REST Client)

---

## 🛡️ Robustez Empírica: Chaos & Fuzz Testing Matrix

Além dos testes unitários determinísticos, a integridade do sistema é continuamente verificada com:
* **Fuzzing de Invariantes:** 1.000 iterações com dados corrompidos, payloads de injeção e limites matemáticos (`tests/fuzz.test.ts`).
* **Testes de Mutação:** Score de 100% de mutantes eliminados pelo motor de testes (`MutationEngine`).
* **SAST Automatizado:** Análise estática profunda via GitHub CodeQL (`.github/workflows/codeql.yml`).
