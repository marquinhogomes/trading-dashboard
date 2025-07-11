print("Test basic import...")
try:
    from config_real import DEPENDENTE_REAL
    print(f"OK: {len(DEPENDENTE_REAL)} dependentes")
except Exception as e:
    print(f"Error: {e}")
