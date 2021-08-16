# Padaria-Case

Iremos simular um caso de uso de uma padaria com centenas de filiais espalhadas pelo mundo, para suportar esse workload utilizaremos uma arquitetura de dados moderna e escalavel com a Cloud da Microsoft.

O que veremos nessa lab:

- Gerar dados FAKE com Python
- Ingestão dos dados gerados por cada filial (Dados no formato JSON)
- Ingestão será toda feita pelo Azure Event Hubs
- Processar e extrair os dados streaming com o Azure Stream Analytics
- Armazenar os dados processados no Azure Cosmos DB para consumo das APIS
- Armazenar os dados processados no Azure SQL Database para consumo do ERP centralizado
- Armazenar os dados no Data lake, gravar no container Bronze no formato parquet
- Processar os dados com o Databricks, extrair dados da camada Bronze, aplicar limpeza dos dados e armazenar na camada Silver no formato delta
- Processar dados da camada Silver para camada Gold com as visões para consumo dos usuários finais
- Criar integração com Github
- Automatizar deploy com git actions

![image](https://user-images.githubusercontent.com/69867503/127775629-baccbd27-67cb-4a6c-a1bb-88c8c093079c.png)

