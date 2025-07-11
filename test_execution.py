#!/usr/bin/env python3
# Test script to check execution
print("✅ Script execution test successful!")
print("Python is working correctly.")

# Check streamlit import
try:
    import streamlit as st
    print("✅ Streamlit import successful!")
except ImportError as e:
    print(f"❌ Streamlit import failed: {e}")

# Check trading modules
try:
    from trading_real_integration import real_state
    print("✅ Trading integration import successful!")
except ImportError as e:
    print(f"❌ Trading integration import failed: {e}")

print("Test completed!")
