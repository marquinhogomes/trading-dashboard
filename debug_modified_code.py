#!/usr/bin/env python3
"""
Debug script to see what the modified code looks like
"""

import sistema_integrado

def debug_modified_code():
    """Debug what the modified code looks like"""
    
    print("=== DEBUGGING MODIFIED CODE ===")
    
    # Create a system instance
    sistema = sistema_integrado.SistemaIntegrado()
    
    # Read the original file
    with open('calculo_entradas_v55.py', 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Apply the same logic as in executar_sistema_original
    linhas_codigo = codigo.split('\n')
    codigo_sem_loop = []
    dentro_bloco_main = False
    dentro_while_true = False
    nivel_indentacao_main = 0
    nivel_indentacao_while = 0
    
    for i, linha in enumerate(linhas_codigo):
        # Detecta o início do bloco if __name__ == "__main__":
        if 'if __name__ == "__main__":' in linha:
            dentro_bloco_main = True
            nivel_indentacao_main = len(linha) - len(linha.lstrip())
            # Substitui por uma execução controlada
            codigo_sem_loop.append('# Sistema original executado pelo sistema_integrado.py')
            codigo_sem_loop.append('# Loop principal removido para evitar execução infinita')
            continue
        
        # Se estamos dentro do bloco main, verifica se saímos dele
        if dentro_bloco_main:
            indentacao_atual = len(linha) - len(linha.lstrip())
            # Se a linha não está vazia e tem indentação menor ou igual ao main, saímos do bloco
            if linha.strip() and indentacao_atual <= nivel_indentacao_main:
                dentro_bloco_main = False
                codigo_sem_loop.append(linha)
                print(f"   Saindo do bloco main na linha {i+1}")
            # Se ainda estamos dentro do bloco main, pula loops infinitos
            elif 'while True:' in linha:
                print(f"🚫 Loop infinito detectado na linha {i+1} dentro do bloco main")
                dentro_while_true = True
                nivel_indentacao_while = len(linha) - len(linha.lstrip())
                print(f"   Indentação do while: {nivel_indentacao_while}")
                codigo_sem_loop.append('# Loop infinito removido pelo sistema_integrado')
                codigo_sem_loop.append('# Conteúdo do loop executado uma única vez:')
                continue
            else:
                # Inclui outras linhas do bloco main (exceto loops infinitos)
                if 'print(' in linha and ('Ciclo completo' in linha or 'Reiniciando' in linha):
                    continue  # Pula prints de loop
                
                # Se estamos dentro do while True, ajustar indentação
                if dentro_while_true:
                    indentacao_atual = len(linha) - len(linha.lstrip())
                    if linha.strip() == '':
                        # Linha vazia, manter
                        codigo_sem_loop.append(linha)
                    elif indentacao_atual <= nivel_indentacao_while:
                        # Saímos do while True
                        dentro_while_true = False
                        codigo_sem_loop.append(linha)
                        print(f"   Saindo do while True na linha {i+1}")
                    else:
                        # Linha dentro do while True, ajustar indentação
                        if linha.strip():
                            # Reduzir indentação em 4 espaços (nível do while)
                            nova_linha = linha[4:] if linha.startswith('    ') else linha.lstrip()
                            # Manter a indentação original sem adicionar extra
                            codigo_sem_loop.append(nova_linha)
                            print(f"   Ajustando linha {i+1}: {repr(linha)} -> {repr(nova_linha)}")
                        else:
                            codigo_sem_loop.append(linha)
                else:
                    codigo_sem_loop.append(linha)
        # Se não estamos no bloco main, verificar se há while True no final do arquivo
        elif 'while True:' in linha and not linha.strip().startswith('#') and i > 6000:
            print(f"🚫 Loop infinito no final do arquivo detectado na linha {i+1}")
            dentro_while_true = True
            nivel_indentacao_while = len(linha) - len(linha.lstrip())
            print(f"   Indentação do while: {nivel_indentacao_while}")
            # Adicionar um comentário no lugar do while
            codigo_sem_loop.append('# Loop infinito removido pelo sistema_integrado')
            codigo_sem_loop.append('# Conteúdo do loop executado uma única vez:')
            continue
        elif dentro_while_true:
            # Estamos processando o conteúdo do while True
            indentacao_atual = len(linha) - len(linha.lstrip())
            if linha.strip() == '':
                # Linha vazia, manter
                codigo_sem_loop.append(linha)
            elif indentacao_atual <= nivel_indentacao_while:
                # Saímos do while True
                dentro_while_true = False
                codigo_sem_loop.append(linha)
            else:
                # Linha dentro do while True, ajustar indentação
                if linha.strip():
                    # Reduzir indentação em 4 espaços (nível do while)
                    nova_linha = linha[4:] if linha.startswith('    ') else linha.lstrip()
                    # Adicionar indentação mínima para manter estrutura
                    nova_linha = '    ' + nova_linha
                    codigo_sem_loop.append(nova_linha)
                    print(f"   Linha {i+1}: {repr(linha)} -> {repr(nova_linha)}")
                else:
                    codigo_sem_loop.append(linha)
        else:
            codigo_sem_loop.append(linha)
    
    # Show the problematic area
    print("\n=== CÓDIGO MODIFICADO PRÓXIMO À LINHA 6310 ===")
    linhas_modificadas = codigo_sem_loop
    
    for i, linha in enumerate(linhas_modificadas[6305:6315], 6306):
        print(f"Line {i:4d}: {repr(linha)}")

if __name__ == "__main__":
    debug_modified_code()
