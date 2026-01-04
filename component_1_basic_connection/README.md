# Component 1: Basic Gemini Connection

**Goal:** Make your first API call and understand the request/response structure  
**Learn:** API setup, prompt format, response handling  
**Output:** Simple question-answer interaction

## What You'll Build

A simple script that:
1. Connects to Google's Gemini API
2. Sends a question to the AI model
3. Receives and displays the response
4. Shows response metadata for debugging

This is the foundation that every AI agent builds upon.

## Setup

### 1. Get Your API Key
- Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
- Sign in with Google
- Click "Create API Key"
- Copy the key

### 2. Install Dependencies
```bash
pip install google-generativeai
```

### 3. Set Environment Variable
```bash
# Windows (PowerShell)
$env:GOOGLE_API_KEY="your-key-here"

# Windows (CMD)
set GOOGLE_API_KEY=your-key-here

# Mac/Linux
export GOOGLE_API_KEY="your-key-here"
```

## Files in This Component

- `basic_connection.py` - Main implementation with detailed comments
- `check_models.py` - Utility script to list available models for your API key
- `README.md` - This guide
- `FAQ.md` - Common issues and solutions (check this if you run into problems!)

## Running the Code

### Check Available Models (Optional)
First, see what models are available for your API key:
```bash
python check_models.py
```

This will show you all available models and which ones support `generateContent`.

### Run the Main Component
```bash
python basic_connection.py
```

Expected output:
```
======================================================================
COMPONENT 1: Basic Gemini API Connection
======================================================================

🔍 Checking available models...

📋 Available Models:
--------------------------------------------------
Model: models/gemini-2.5-flash
  Display Name: Gemini 2.5 Flash
  Status: ✓ Supports generateContent
  Methods: generateContent, countTokens, createCachedContent, batchGenerateContent
--------------------------------------------------
[... more models ...]

✓ Using model: models/gemini-2.5-flash
✓ Gemini API configured successfully!

📤 Sending question: Explain what an AI agent is in 2-3 sentences.

======================================================================
📥 GEMINI RESPONSE:
======================================================================
An AI agent is a software program that can perceive its environment,
make decisions, and take actions to achieve specific goals. Unlike
traditional programs that follow rigid instructions, agents can
adapt their behavior based on changing conditions and learn from
their experiences. They often use machine learning models to
understand context and determine the best course of action.
======================================================================

📊 Response Metadata:
   - Number of candidates: 1
   - Finish reason: STOP
   - Safety ratings: 4 checks

✅ Component 1 Complete!

What you learned:
  ✓ How to configure Gemini API
  ✓ How to make a basic API call
  ✓ How to parse and display responses

Next: Component 2 will add tool calling (functions)
```

## What You're Learning

### 1. The Request-Response Pattern
Every agent interaction follows this basic pattern:
```python
response = model.generate_content(question)
```
This is the foundation. Everything builds on this.

### 2. Response Structure
The response object contains:
- `text` - The generated content
- `candidates` - Possible responses (usually just one)
- `finish_reason` - Why it stopped (STOP, MAX_TOKENS, etc.)
- `safety_ratings` - Content safety checks

### 3. Model Selection
We automatically select the best available model, preferring:
- `models/gemini-2.5-flash` - Fast and efficient
- `models/gemini-2.0-flash` - Good fallback
- `models/gemini-flash-latest` - Always current

### 4. Error Handling Basics
The code handles common issues:
- Missing API key
- No available models
- API connection problems

## Troubleshooting

### "No API key found"
Make sure you've set the environment variable correctly:
```bash
echo $GOOGLE_API_KEY  # Mac/Linux
echo $env:GOOGLE_API_KEY  # Windows PowerShell
```

### "404 models/[model-name] is not found"
Run `python check_models.py` to see what models are actually available for your API key. The script will automatically use the first working model it finds.

### "No models support generateContent"
This usually means there's an issue with your API key or account. Double-check:
1. API key is correct
2. You have API access enabled
3. You're not hitting rate limits

**For more detailed troubleshooting, see [FAQ.md](FAQ.md) - it covers all the common issues we encountered while building this component.**

## Experiments to Try

Before moving to Component 2, try these experiments:

1. **Different Questions**: Try various types of questions and see how responses differ
2. **Long Prompts**: What happens with very long input?
3. **Empty Input**: How does the model handle empty strings?
4. **Multiple Calls**: Run the script several times - are responses consistent?

## Key Concepts

This component introduces the fundamental concepts you'll use throughout the series:

- **API Configuration**: How to authenticate and connect
- **Model Selection**: Choosing the right model for your needs
- **Request Structure**: How to format input for the model
- **Response Parsing**: How to extract and use the model's output
- **Error Handling**: Basic patterns for robust code

## Next Steps

In Component 2, we'll add our first tool and teach the agent when to use it. This is where things get interesting - the agent will start making autonomous decisions about when to search the web versus answering from its knowledge.

That's when it becomes a true agent, not just a chatbot.

## Code Structure

The main script follows this pattern:
1. **Setup**: Configure API and select model
2. **Request**: Send question to model
3. **Response**: Parse and display results
4. **Metadata**: Show debugging information

This structure scales to more complex agents - we just add more steps between Request and Response.

---

**Ready for Component 2?** Head back to the main README to continue the journey!