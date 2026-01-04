#!/usr/bin/env python3
"""
Quick script to check available Gemini models for your API key
Usage: python check_models.py
"""

import os
import google.generativeai as genai

def main():
    # Get API key
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in environment!")
        print("Set it with: export GOOGLE_API_KEY='your-key-here'")
        return
    
    # Configure API
    genai.configure(api_key=api_key)
    
    try:
        print("🔍 Fetching available models for your API key...\n")
        models = list(genai.list_models())  # Convert to list first
        
        print("📋 AVAILABLE MODELS:")
        print("=" * 80)
        
        generate_models = []
        
        for model in models:
            supports_generate = 'generateContent' in model.supported_generation_methods
            
            print(f"Model Name: {model.name}")
            print(f"Display Name: {model.display_name}")
            print(f"Supports generateContent: {'✓ YES' if supports_generate else '✗ NO'}")
            print(f"All Methods: {', '.join(model.supported_generation_methods)}")
            
            if supports_generate:
                generate_models.append(model.name)
            
            print("-" * 80)
        
        print(f"\n🎯 MODELS YOU CAN USE (support generateContent):")
        if generate_models:
            for model_name in generate_models:
                print(f"  ✓ {model_name}")
        else:
            print("  ❌ No models support generateContent!")
            
        print(f"\nTotal models available: {len(models)}")
        print(f"Models supporting generateContent: {len(generate_models)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nPossible issues:")
        print("  - Invalid API key")
        print("  - Network connectivity")
        print("  - API quota exceeded")

if __name__ == "__main__":
    main()