"""
COMPONENT 1: Basic Gemini Connection
====================================
Goal: Make your first API call and understand the request/response structure
Learn: API setup, prompt format, response handling
Output: Simple question-answer interaction

SETUP:
1. Install: pip install google-generativeai
2. Get API key from: https://aistudio.google.com/app/apikey
3. Set environment variable: export GOOGLE_API_KEY="your-key-here"
   Or pass directly in code (for testing only)
"""

import os
import google.generativeai as genai

# ============================================================================
# STEP 1: Configure the API
# ============================================================================
def list_available_models():
    """
    List all available models for your API key.
    This helps debug model availability issues.
    """
    try:
        print("🔍 Checking available models...")
        models = list(genai.list_models())  # Convert to list first
        
        print("\n📋 Available Models:")
        print("-" * 50)
        
        for model in models:
            # Check if model supports generateContent
            supports_generate = 'generateContent' in model.supported_generation_methods
            status = "✓ Supports generateContent" if supports_generate else "✗ No generateContent"
            
            print(f"Model: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Status: {status}")
            print(f"  Methods: {', '.join(model.supported_generation_methods)}")
            print("-" * 50)
            
        return models
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return None


# ============================================================================
# STEP 1: Configure the API
# ============================================================================
def setup_gemini():
    """
    Initialize the Gemini API with your credentials.
    
    Returns:
        model: Configured Gemini model instance
    """
    # Get API key from environment variable (recommended)
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found in environment!")
        print("Get your key from: https://aistudio.google.com/app/apikey")
        print("Then run: export GOOGLE_API_KEY='your-key-here'")
        return None
    
    # Configure the SDK
    genai.configure(api_key=api_key)
    
    # First, let's see what models are available
    models = list_available_models()
    if not models:
        return None
    
    # Try to find a working model
    working_models = []
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            working_models.append(model.name)
    
    if not working_models:
        print("❌ No models support generateContent!")
        return None
    
    # Use gemini-2.5-flash if available, otherwise use the first available model
    preferred_models = ['models/gemini-2.5-flash', 'models/gemini-2.0-flash', 'models/gemini-flash-latest']
    model_name = None
    
    for preferred in preferred_models:
        if preferred in working_models:
            model_name = preferred
            break
    
    if not model_name:
        model_name = working_models[0]
    
    print(f"\n✓ Using model: {model_name}")
    
    # Initialize the model
    model = genai.GenerativeModel(model_name)
    
    print("✓ Gemini API configured successfully!")
    print(f"✓ Using model: {model_name}\n")
    
    return model


# ============================================================================
# STEP 2: Make a Simple Request
# ============================================================================
def ask_question(model, question):
    """
    Send a question to Gemini and get a response.
    
    Args:
        model: Gemini model instance
        question: String question to ask
        
    Returns:
        response: Model's response object
    """
    print(f"📤 Sending question: {question}\n")
    
    # Generate content - this is the core API call
    response = model.generate_content(question)
    
    return response


# ============================================================================
# STEP 3: Parse and Display the Response
# ============================================================================
def display_response(response):
    """
    Extract and display the model's response.
    
    The response object contains:
    - text: The actual generated text
    - candidates: All possible responses (usually just one)
    - prompt_feedback: Safety ratings, etc.
    """
    print("=" * 70)
    print("📥 GEMINI RESPONSE:")
    print("=" * 70)
    print(response.text)
    print("=" * 70)
    
    # Show response metadata (useful for debugging)
    print("\n📊 Response Metadata:")
    print(f"   - Number of candidates: {len(response.candidates)}")
    print(f"   - Finish reason: {response.candidates[0].finish_reason}")
    print(f"   - Safety ratings: {len(response.candidates[0].safety_ratings)} checks")


# ============================================================================
# MAIN: Put it all together
# ============================================================================
def main():
    """
    Component 1 Demo: Basic connection and simple Q&A
    """
    print("\n" + "=" * 70)
    print("COMPONENT 1: Basic Gemini API Connection")
    print("=" * 70 + "\n")
    
    # Step 1: Setup
    model = setup_gemini()
    if not model:
        return
    
    # Step 2: Ask a simple question
    question = "Explain what an AI agent is in 2-3 sentences."
    response = ask_question(model, question)
    
    # Step 3: Display the response
    display_response(response)
    
    print("\n✅ Component 1 Complete!")
    print("\nWhat you learned:")
    print("  ✓ How to configure Gemini API")
    print("  ✓ How to make a basic API call")
    print("  ✓ How to parse and display responses")
    print("\nNext: Component 2 will add tool calling (functions)")


# ============================================================================
# Run the component
# ============================================================================
if __name__ == "__main__":
    main()