Para resolver o problema de desempenho em que a extração e análise de dados estão atrasando o monitoramento de lucros e outras operações, você pode considerar algumas abordagens:

### 1. **Multithreading ou Processamento Assíncrono**
Utilize multithreading ou processamento assíncrono para separar as tarefas de extração/análise de dados e monitoramento. Isso permitirá que ambas as operações sejam executadas simultaneamente, sem que uma bloqueie a outra.

- **Multithreading**: Crie uma thread separada para a extração e análise de dados. A thread principal pode ser responsável pelo monitoramento.
- **Assíncrono**: Se a linguagem de programação que você está usando suporta programação assíncrona (como Python com `asyncio`), você pode usar essa abordagem para não bloquear a execução.

### 2. **Divisão de Tarefas**
Divida as tarefas em partes menores e execute-as em intervalos regulares. Por exemplo, em vez de fazer uma análise completa de dados a cada execução, você pode fazer uma análise parcial e, em seguida, monitorar os lucros.

### 3. **Uso de Filas**
Implemente um sistema de filas para gerenciar as tarefas. Você pode ter uma fila para a extração/análise de dados e outra para o monitoramento. Isso permite que as tarefas sejam processadas de forma independente.

### 4. **Otimização de Código**
Revise o código da parte de extração e análise para identificar gargalos de desempenho. Algumas otimizações podem incluir:
- Reduzir a quantidade de dados processados.
- Melhorar algoritmos de análise.
- Utilizar bibliotecas otimizadas para operações pesadas.

### 5. **Cache de Resultados**
Se a análise de dados não precisa ser feita em tempo real, considere armazenar os resultados em cache. Assim, você pode usar os dados em cache para o monitoramento, evitando a necessidade de recalcular a cada execução.

### 6. **Ajuste de Frequência**
Ajuste a frequência com que as operações de monitoramento e análise são realizadas. Por exemplo, você pode realizar a análise de dados a cada 5 minutos, enquanto o monitoramento é feito a cada 1 minuto.

### 7. **Separação de Serviços**
Se o sistema for complexo o suficiente, considere separar as funcionalidades em serviços distintos (por exemplo, usando microserviços). Isso pode permitir que cada serviço seja escalado e otimizado de forma independente.

### 8. **Uso de Banco de Dados**
Se você estiver lidando com grandes volumes de dados, considere usar um banco de dados para armazenar e consultar os dados de forma mais eficiente. Isso pode ajudar a acelerar a extração e análise.

### Implementação
Escolha uma ou mais dessas abordagens que se encaixem melhor no seu contexto e comece a implementar. Teste as mudanças para garantir que o desempenho do monitoramento melhore sem comprometer a qualidade da análise de dados.