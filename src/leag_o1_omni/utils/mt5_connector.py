Para resolver o problema de desempenho em que a extração e análise de dados estão atrasando o monitoramento de lucros e outras operações, você pode considerar algumas abordagens:

### 1. **Multithreading ou Processamento Assíncrono**
   - **Multithreading**: Execute a extração e análise de dados em uma thread separada. Isso permitirá que o monitoramento continue a rodar em paralelo, sem ser bloqueado pela análise de dados.
   - **Processamento Assíncrono**: Se a linguagem de programação que você está usando suporta programação assíncrona (como Python com `asyncio`), você pode implementar chamadas assíncronas para que a análise de dados não bloqueie o fluxo principal do monitoramento.

### 2. **Divisão de Tarefas**
   - **Batch Processing**: Em vez de processar todos os dados de uma vez, divida a extração e análise em lotes menores. Isso pode ajudar a reduzir o tempo de espera e permitir que o monitoramento seja feito em intervalos regulares.
   - **Prioridade de Tarefas**: Dê prioridade ao monitoramento em relação à extração de dados. Você pode implementar um sistema de filas onde as tarefas de monitoramento são processadas antes das tarefas de análise.

### 3. **Otimização de Código**
   - **Melhorar a Eficiência**: Revise o código de extração e análise para identificar gargalos de desempenho. Otimize consultas a bancos de dados, utilize algoritmos mais eficientes e minimize operações desnecessárias.
   - **Cache de Resultados**: Se os dados não mudam com frequência, considere armazenar em cache os resultados da análise para evitar recalcular a mesma informação repetidamente.

### 4. **Uso de Serviços Externos**
   - **Microserviços**: Se a arquitetura permitir, você pode separar a extração/análise e o monitoramento em microserviços diferentes. Isso permite que cada serviço seja escalado independentemente e pode melhorar a performance geral.
   - **Filas de Mensagens**: Utilize um sistema de filas (como RabbitMQ ou Kafka) para desacoplar a extração/análise do monitoramento. O monitoramento pode consumir mensagens de uma fila enquanto a análise é feita em segundo plano.

### 5. **Ajuste de Frequência**
   - **Intervalos de Monitoramento**: Ajuste a frequência com que o monitoramento é realizado. Se a análise de dados é feita em intervalos maiores, você pode monitorar com mais frequência, garantindo que as operações abertas sejam verificadas rapidamente.

### 6. **Feedback Visual**
   - **Indicadores de Progresso**: Se a análise de dados leva tempo, considere implementar um feedback visual (como uma barra de progresso) para que os usuários saibam que a análise está em andamento, enquanto o monitoramento continua.

Implementando uma ou mais dessas abordagens, você deve conseguir melhorar a performance do seu sistema, garantindo que a extração e análise de dados não atrapalhem o monitoramento das operações abertas.