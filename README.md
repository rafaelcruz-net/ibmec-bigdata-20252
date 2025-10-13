# Chatbot de Reservas de Hotéis e Voos 

## Equipe
|Matrícula | Aluno |
| -- | -- |
| 202401000991  |  Fellipe Martins Valladares|
| 202401000981  |  João Pedro Martins Abdu |

## Objetivo do Projeto
O projeto consiste no desenvolvimento de um **chatbot inteligente** capaz de permitir que usuários pesquisem e realizem reservas de **hotéis** e **passagens aéreas** por meio de mensagens em linguagem natural.  
Ele utiliza **Azure Bot Framework**, **LUIS** para processamento de linguagem natural (NLP), **Text Analytics** para análise de sentimento e integração com **APIs externas** para consulta de disponibilidade.

O chatbot será capaz de:
- Entender intenções do usuário;
- Consultar informações de hotéis e voos em APIs públicas/gratuitas;
- Analisar sentimentos para identificar satisfação ou frustração;
- Armazenar histórico de conversas e métricas de uso.

---

##  Escopo do Sistema

### Funcionalidades Principais
-  **Interação com o usuário** via Chat (WebChat, Microsoft Teams e opcionalmente Telegram);
-  **Processamento de Linguagem Natural (LUIS)** para identificar intenções e extrair entidades;
-  **Análise de Sentimento** com Azure Text Analytics;
-  **Consulta a APIs** de Hotéis e Voos:
  - Hotelbeds, Amadeus, Skyscanner, Kiwi Tequila;
-  **Armazenamento de dados** no Azure Cosmos DB;
-  **Relatórios e métricas** no Power BI.

---

##  Arquitetura do Sistema

### Componentes Azure Utilizados
- **Azure Bot Service + Bot Framework SDK**
- **Azure Cognitive Services** (LUIS e Text Analytics)
- **Azure Functions** (serverless)
- **Azure Cosmos DB**
- **Power BI Embedded**

### Fluxo de Mensagem
1. Usuário envia mensagem (ex.: *"Quero um voo para São Paulo amanhã à noite"*).
2. **Bot Framework** encaminha para **LUIS**.
3. **LUIS** retorna intenção e entidades.
4. **Text Analytics** avalia o sentimento.
5. **Azure Function** consulta APIs de voos/hotéis e retorna opções.
6. Bot envia opções ao usuário e armazena histórico da conversa.

---

##  Integração com APIs

### APIs de Hotéis
- **Hotelbeds API** (Sandbox, limite de 50 chamadas/dia)
- **Amadeus Self-Service Hotel API** (limite gratuito mensal)

### APIs de Voos
- **Skyscanner API** (via RapidAPI)
- **Kiwi Tequila** (sandbox)

---

##  Requisitos Não Funcionais
- **Disponibilidade:** 99,5%
- **Escalabilidade:** utilização de Azure Functions para lidar com picos de requisição

---

##  Tecnologias e Ferramentas
- **Linguagens:** C#, Java, Node.js, Python (compatível com Bot Framework)
- **Banco de Dados:** Azure Cosmos DB ou SQL Database
- **Ferramentas:** VS Code / Visual Studio, Postman, Azure Portal

---

##  Critérios de Aceite
- Chatbot entende pelo menos **5 intenções principais**;
- Integração com pelo menos **1 API de hotel** e **1 API de voo**;
- Histórico de conversas armazenado junto com análise de sentimento.

---
##  Fluxograma
<img src="Documentação/Fluxograma.png" alt="Fluxograma"/>
