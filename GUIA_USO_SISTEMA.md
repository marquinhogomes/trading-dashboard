# 🚀 GUIA DE USO DO SISTEMA - SEQUÊNCIA CORRETA

## **📋 SEQUÊNCIA COMPLETA PARA USAR O SISTEMA:**

### **1. 🖥️ INICIAR O DASHBOARD:**
```bash
streamlit run dashboard_trading_pro_real.py
```

### **2. 🌐 NO NAVEGADOR - SEQUÊNCIA DOS BOTÕES:**

#### **📍 ETAPA 1: CONECTAR AO MT5**
1. No **sidebar esquerdo**, encontre a seção **"🔌 MetaTrader 5"**
2. Preencha os campos:
   - **Login**: Seu login do MT5
   - **Senha**: Sua senha do MT5
   - **Servidor**: Seu servidor (ex: Rico-Real, XM-Real, etc.)
3. Clique no botão **"Conectar"**
4. ✅ **Aguarde aparecer "Conectado"** (botão verde)

#### **📍 ETAPA 2: CONFIGURAR PARÂMETROS (OPCIONAL)**
1. No **sidebar**, ajuste os parâmetros se necessário:
   - **Máximo de Posições**: Quantas posições simultâneas
   - **Valor por Operação**: Valor em R$ por operação
   - **Horário de Finalização**: Quando parar de enviar ordens
   - **Filtros**: R², Beta, Cointegração, etc.
2. Se alterar algum parâmetro, aparecerá o botão **"🔄 Aplicar Parâmetros Agora"**
3. Você pode:
   - **Opção A**: Clicar em **"🔄 Aplicar Parâmetros Agora"** (aplicação imediata)
   - **Opção B**: Pular para a próxima etapa (aplicação automática)

#### **📍 ETAPA 3: INICIAR O SISTEMA**
1. No **sidebar**, encontre a seção **"🎮 Plataforma"**
2. Clique no botão **"Iniciar Análise"**
3. ✅ **Aguarde aparecer "Análise iniciada em background"**
4. O botão mudará para **"Parar Análise"** (sistema rodando)

### **3. 🔄 SISTEMA FUNCIONANDO:**
- ✅ **Sistema executando automaticamente** em background
- ✅ **Logs aparecendo** na aba "Logs do Sistema"
- ✅ **Tabelas sendo geradas** nas abas "Pares Validados" e "Sinais"
- ✅ **Posições sendo monitoradas** na aba "Posições"

### **4. 🛑 PARA PARAR O SISTEMA:**
1. No **sidebar**, na seção **"🎮 Plataforma"**
2. Clique no botão **"Parar Análise"**
3. ✅ **Sistema será interrompido** e o botão voltará para "Iniciar Análise"

---

## **🔍 DIAGNÓSTICO DE PROBLEMAS:**

### **❌ Botão "Iniciar Análise" Desabilitado:**
- **Causa**: MT5 não conectado
- **Solução**: Volte para ETAPA 1 e conecte ao MT5

### **❌ Botão "Backend Indisponível":**
- **Causa**: Sistema integrado com erro
- **Solução**: Reinicie o dashboard (Ctrl+C e rode novamente)

### **❌ Análise não inicia:**
- **Causa**: Erro no sistema integrado
- **Solução**: Verifique logs na aba "Logs do Sistema"

### **❌ Parâmetros não aplicados:**
- **Causa**: Parâmetros não foram salvos
- **Solução**: Clique em "🔄 Aplicar Parâmetros Agora" antes de iniciar

---

## **📝 RESUMO DA SEQUÊNCIA:**

1. **Conectar** → MT5 (botão verde "Conectado")
2. **Configurar** → Parâmetros (opcional)
3. **Iniciar** → Análise (botão "Iniciar Análise")
4. **Monitorar** → Dashboard (tabelas e logs)
5. **Parar** → Análise (botão "Parar Análise")

**🎯 ORDEM CORRETA: MT5 → Parâmetros → Iniciar Análise**

---
*Sistema configurado e pronto para uso!*
