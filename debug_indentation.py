#!/usr/bin/env python3
"""
Debug script to understand the indentation issue in the calculo_entradas_v55.py file
"""

def debug_indentation_issue():
    """Debug the indentation issue around line 6310"""
    
    with open('calculo_entradas_v55.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print("=== DEBUGGING INDENTATION ISSUE ===")
    print("Checking lines around 6310...")
    
    start_line = 6305
    end_line = 6315
    
    for i in range(start_line-1, min(end_line, len(lines))):
        line = lines[i]
        indent_count = len(line) - len(line.lstrip())
        print(f"Line {i+1:4d} (indent={indent_count:2d}): {repr(line.rstrip())}")
    
    print("\n=== FINDING THE WHILE TRUE CONTEXT ===")
    
    # Find the while True and its context
    for i, line in enumerate(lines):
        if 'while True:' in line and not line.strip().startswith('#') and i > 6000:
            print(f"\nFound while True at line {i+1}:")
            print(f"Line {i+1}: {repr(line.rstrip())}")
            print(f"Indentation: {len(line) - len(line.lstrip())} spaces")
            
            print("\nContext before:")
            for j in range(max(0, i-3), i):
                context_line = lines[j]
                indent = len(context_line) - len(context_line.lstrip())
                print(f"Line {j+1:4d} (indent={indent:2d}): {repr(context_line.rstrip())}")
            
            print("\nContext after:")
            for j in range(i+1, min(len(lines), i+6)):
                context_line = lines[j]
                indent = len(context_line) - len(context_line.lstrip())
                print(f"Line {j+1:4d} (indent={indent:2d}): {repr(context_line.rstrip())}")
            
            break

if __name__ == "__main__":
    debug_indentation_issue()
