<div align="center">

<p align="center">

  <a href="" rel="noopener">

<img width=300px height=256px src="./preview.webp" alt="job logo"></a>

</p>
 
<h3 align="center">JOB HERO - Langflow Desafio 4</h3>

</div>
 
<div align="center">
 
  [![Status](https://img.shields.io/badge/status-active-success.svg)]()

  [![GitHub Issues](https://img.shields.io/github/issues/AndreViniNe/langflow-desafio4.svg)](https://github.com/AndreViniNe/langflow-desafio4/issues)

  [![GitHub Pull Requests](https://img.shields.io/github/issues-pr/AndreViniNe/langflow-desafio4.svg)](https://github.com/AndreViniNe/langflow-desafio4/pulls)

 
</div>

## 📝 Tabela de conteúdos
+ [Desafio](#desafio)

+ [Contexto](#contexto)

+ [Proposta](#proposta)

+ [Autores](#autores)


## 🏆 Desafio <a name = "desafio"></a>
- Criar uma aplicação no langflow de ponta a ponta com tema livre com todos os temas aprendidos até o momento nas outras
etapas da competição
    * RAG
    * Agentes
    * Prompt Engineering

## 📖 Contexto <a name = "contexto"></a>
- Atualmente, há uma grande dificuldade de achar as vagas certas para a sua posição e experiência, dificultado mais ainda
por filtros das vagas, como data da postagem, localização, modalidade etc.
- E para tantas vagas, candidatar em todas as que aparecem leva muito tempo

## 💡 Proposta <a name = "proposta"></a>
- Um flow automatizado, que recebe
    * Currículo de link do Linkedin
    * Filtros de trabalho (preferências)
- Com essas informações, uma IA automaticamento busca as vagas que se encaixam nas preferências e experiências do usuário
e se candidata automaticamente nelas, economizando muito tempo investido nessas procuras

## 📄 Repositório <a name = "repositorio"></a>

### Fluxos Langflow

- [Extractor Agent](./langflow/extractor_agent.json): Responsável por coletar dados de fontes: Linkedin (Jobs e Posts) e Cia Talentos.
- [Extractor Agent Loop](./langflow/extractor_loop.json): Responsável por iterar a execução do Extractor Agent para a coleta de vagas.
- [Job Searcher Agent](./langflow/jobsearcher_agent.json): Responsável por coletar perfil do usuários e buscar vagas no vector store da Datastax AstraDB.
- [Retriever Vector Store](./langflow/retriever_vector_store.json): Flow as a Tool de suporte para retrieve vector store Datastax AstraDB.
- [Save to Vector Store](./langflow/save_to_vector_store.json): Flow as a Tool de suporte para armazenamento no vector store Datastax AstraDB.

### App Streamlit

- [App Job Hero](./app_streamlit.py): App desenvolvimento em streamlit para interface de usuário e trigger API Langflow.
- [Database info](./database_infos.py): Informações de acesso banco de dados Postgresql

## ✍️ Autores <a name = "autores"></a>

- [@André Vinícius](https://github.com/AndreViniNe)
- [@Guilherme Neves](https://github.com/guilhermeneves)