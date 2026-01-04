# Component 1: Frequently Asked Questions

This FAQ captures common issues and lessons learned when running Component 1. These are real problems that developers encounter when getting started with AI agents.

## Environment Setup Issues

### Q: How do I set environment variables on different operating systems?

**A:** Environment variables work differently on each OS:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-key-here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your-key-here
```

**Mac/Linux (Bash/Zsh):**
```bash
export GOOGLE_API_KEY="your-key-here"
```

**To make it permanent:**
- **Windows**: Add to System Environment Variables through Control Panel
- **Mac/Linux**: Add the export line to your `~/.bashrc` or `~/.zshrc` file

### Q: How can I verify my environment variable is set correctly?

**A:** Check if it's set:

**Windows (PowerShell):**
```powershell
echo $env:GOOGLE_API_KEY
```

**Windows (CMD):**
```cmd
echo %GOOGLE_API_KEY%
```

**Mac/Linux:**
```bash
echo $GOOGLE_API_KEY
```

If it shows your API key, it's set correctly. If it's empty or shows the variable name, it's not set.

## Model Availability Issues

### Q: Why did I get "404 models/gemini-1.5-flash is not found"?

**A:** This is the most common issue when starting with Gemini API. The problem is that model names change over time and availability varies by region and API access level.

**What happened:**
- The original code used `gemini-1.5-flash`
- This model name isn't available in all regions or API tiers
- Google's model naming and availability changes frequently

**How we solved it:**
1. Created `check_models.py` to list actually available models
2. Updated the main script to automatically select the first working model
3. Added fallback logic to try multiple model names

### Q: How do I find out which models are available for my API key?

**A:** Run the model checker utility:

```bash
python check_models.py
```

This will show you:
- All models available for your specific API key
- Which ones support `generateContent` (what we need)
- The exact model names to use

**Example output:**
```
Model: models/gemini-2.5-flash
Display Name: Gemini 2.5 Flash
Supports generateContent: ✓ YES
Methods: generateContent, countTokens, createCachedContent, batchGenerateContent
```

## API Connection Issues

### Q: I'm getting authentication errors even though my API key is set

**A:** Check these common issues:

1. **API key format**: Make sure there are no extra spaces or quotes
2. **API key validity**: Test your key at [Google AI Studio](https://aistudio.google.com/)
3. **API access**: Ensure you have access to the Gemini API (some regions have restrictions)
4. **Rate limits**: You might be hitting rate limits if you've made many requests

### Q: The script works sometimes but fails other times

**A:** This usually indicates rate limiting or quota issues:

1. **Free tier limits**: Gemini free tier has daily/hourly limits
2. **Rate limiting**: Too many requests too quickly
3. **Model availability**: Some models have limited availability

**Solution**: Add retry logic and respect rate limits (we'll cover this in Component 6).

## Code Understanding Issues

### Q: What's the difference between the LLM response and what I see printed?

**A:** The response object contains much more than just the text:

```python
response = model.generate_content(question)

# What you see printed
print(response.text)  # Just the generated text

# What's actually in the response
response.candidates[0].finish_reason  # Why it stopped
response.candidates[0].safety_ratings  # Safety checks
response.usage_metadata  # Token usage (if available)
```

Understanding the full response structure helps with debugging and optimization.

### Q: Why do we check `finish_reason`?

**A:** The `finish_reason` tells you why the model stopped generating:

- `STOP`: Natural completion (good)
- `MAX_TOKENS`: Hit token limit (might be truncated)
- `SAFETY`: Blocked by safety filters
- `RECITATION`: Blocked for potential copyright issues

This is crucial for production agents - you need to handle each case differently.

## Development Workflow Issues

### Q: How should I test changes to the code?

**A:** Follow this workflow:

1. **Start small**: Test with simple questions first
2. **Check models**: Run `check_models.py` if you get model errors
3. **Verify environment**: Double-check your API key is set
4. **Read error messages**: The error messages usually tell you exactly what's wrong
5. **Use the metadata**: Check `finish_reason` and safety ratings for debugging

### Q: What should I try after getting Component 1 working?

**A:** Experiment with these variations:

1. **Different question types**: 
   - Factual questions
   - Creative requests
   - Code generation
   - Analysis tasks

2. **Edge cases**:
   - Very long prompts
   - Empty strings
   - Special characters
   - Multiple languages

3. **Response analysis**:
   - Look at safety ratings
   - Check token usage
   - Compare different models

This experimentation builds intuition for how agents behave.

## Performance and Cost Issues

### Q: How much does this cost to run?

**A:** Gemini has a generous free tier:
- 1,500 requests per day
- Rate limit of 15 requests per minute

For Component 1, each run makes 1 request, so you can run it 1,500 times per day for free.

**Cost monitoring tip**: The response object sometimes includes usage metadata showing token counts.

### Q: Which model should I use for learning?

**A:** For learning and development:

1. **gemini-2.5-flash** or **gemini-2.0-flash**: Fast, cheap, good for most tasks
2. **gemini-pro-latest**: More capable but slower/more expensive
3. **Avoid experimental models**: They might change or disappear

The script automatically picks the best available model for your API key.

## Next Steps

### Q: I got Component 1 working - what should I understand before moving on?

**A:** Make sure you understand:

1. **The request-response pattern**: This is the foundation of all agents
2. **Model selection**: How to choose and verify models
3. **Error handling basics**: Reading error messages and response metadata
4. **Environment setup**: Managing API keys securely

### Q: What concepts from Component 1 will I use in later components?

**A:** Everything! Component 1 establishes:

- **API connection patterns** (used in every component)
- **Response parsing** (gets more complex with tools)
- **Error handling** (expanded in Component 6)
- **Model selection** (important for different agent capabilities)

## Troubleshooting Checklist

If something isn't working, check these in order:

1. ✅ **API key set**: `echo $GOOGLE_API_KEY` shows your key
2. ✅ **Dependencies installed**: `pip install google-generativeai`
3. ✅ **Models available**: `python check_models.py` shows working models
4. ✅ **Internet connection**: Can you reach Google's servers?
5. ✅ **Rate limits**: Have you made too many requests recently?
6. ✅ **Code syntax**: Any Python syntax errors?

## Common Error Messages and Solutions

**"GOOGLE_API_KEY not found in environment"**
→ Set your environment variable correctly

**"404 models/[model-name] is not found"**
→ Run `check_models.py` to see available models

**"No models support generateContent"**
→ Usually an API key or account access issue

**"Rate limit exceeded"**
→ Wait a few minutes and try again

**"Safety filter triggered"**
→ Try a different, less sensitive question

---

**Still stuck?** Open an issue in the repository with:
1. Your operating system
2. The exact error message
3. What you were trying to do
4. Output from `check_models.py` (if it runs)

Remember: Getting stuck is part of learning! These issues teach you how real AI systems behave.