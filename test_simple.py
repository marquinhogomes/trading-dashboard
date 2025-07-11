#!/usr/bin/env python3
"""Teste simples das configurações"""

print("Testando config_real...")
from config_real import DEPENDENTE_REAL, SYSTEM_INFO
print(f"✅ {len(DEPENDENTE_REAL)} ativos dependentes carregados")
print(f"✅ Sistema: {SYSTEM_INFO['version']}")

print("Teste concluído com sucesso!")
