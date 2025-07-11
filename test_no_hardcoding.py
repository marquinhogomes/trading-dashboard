"""
Teste automatizado para garantir ausência de hardcodings de parâmetros críticos nos módulos principais.
Este teste percorre os arquivos e verifica se parâmetros críticos são buscados de parametros_dinamicos ou funções utilitárias,
não permitindo valores fixos para parâmetros de negócio.
"""
import re
import os

# Parâmetros críticos que devem ser dinâmicos
PARAMETROS_CRITICOS = [
    'zscore_min', 'zscore_max', 'max_posicoes', 'filtro_cointegracao', 'filtro_r2', 'filtro_beta', 'filtro_zscore',
    'r2_min', 'beta_max', 'coint_pvalue_max', 'valor_operacao', 'valor_operacao_ind', 'limite_lucro', 'limite_prejuizo',
    'intervalo_execucao', 'inicia_pregao', 'finaliza_pregao', 'finaliza_ordens', 'ajusta_ordens', 'horario_ajuste_stops',
    'ajusta_ordens_minuto', 'horario_remove_pendentes', 'horario_fechamento_total',
    'stop_gain_compra_pct', 'stop_loss_compra_pct', 'stop_gain_venda_pct', 'stop_loss_venda_pct'
]

# Arquivos a serem verificados
ARQUIVOS = [
    'dashboard_trading_pro_real.py',
    'sistema_integrado.py',
    'calculo_entradas_v55.py',
]

# Regex para identificar hardcodings suspeitos (números mágicos, valores fixos em funções)
REGEX_HARDCODING = re.compile(r'[^\w](\d{2,}|\d+\.\d+)[^\w]')

# Função para verificar se o parâmetro é buscado de forma dinâmica

def verifica_parametro_dinamico(linha, parametro):
    return (
        f'parametros_dinamicos["{parametro}"]' in linha or
        f'parametros_dinamicos.get("{parametro}"' in linha or
        f'get_parametro_dinamico("{parametro}"' in linha or
        f'self.{parametro}' in linha or
        f'config.get("{parametro}"' in linha
    )

def main():
    erros = []
    for arquivo in ARQUIVOS:
        if not os.path.exists(arquivo):
            continue
        with open(arquivo, encoding='utf-8') as f:
            linhas = f.readlines()
        for i, linha in enumerate(linhas):
            for parametro in PARAMETROS_CRITICOS:
                if parametro in linha:
                    if not verifica_parametro_dinamico(linha, parametro):
                        erros.append(f"[HARDCODING] {arquivo}:{i+1}: Parâmetro '{parametro}' não dinâmico: {linha.strip()}")
            # Busca por números mágicos suspeitos
            if REGEX_HARDCODING.search(linha):
                # Ignora se for comentário ou docstring
                if not linha.strip().startswith('#') and '"""' not in linha:
                    erros.append(f"[MAGIC NUMBER] {arquivo}:{i+1}: {linha.strip()}")
    if erros:
        print("\n\n==== ALERTA: POSSÍVEIS HARDCODINGS DETECTADOS ====")
        for erro in erros:
            print(erro)
        print("\nRevise os pontos acima para garantir centralização dos parâmetros.")
    else:
        print("\nNenhum hardcoding crítico detectado. Parâmetros dinâmicos OK!")

if __name__ == "__main__":
    main()
