# Building AI Agents from First Principles: A Developer's Journey

## Series Introduction: Why Agents Matter Now

We're at an inflection point in software development. AI agents are rapidly moving from experimental prototypes to production systems. What was once the domain of research labs is now becoming standard tooling—from code completion in your IDE to autonomous customer service systems handling millions of interactions.

But here's the problem: most developers are using agents without understanding how they actually work. We're treating them as black boxes, relying on frameworks and abstractions that hide the fundamental mechanics. This works until it doesn't—until you need to debug why your agent is making poor decisions, burning through API costs, or failing on edge cases.

This multi-part series takes a different approach. We're going to build an AI agent from scratch, component by component, understanding every piece along the way. Not because you'll always build from scratch in production, but because understanding the foundations is critical for the world we're entering—a world where agents are infrastructure, not novelties.

By the end of this series, you'll understand:
- How agents actually make decisions (the agent loop)
- How tool calling really works under the hood
- How to manage context and memory effectively
- How to build reliable, production-ready agents
- How to debug and optimize agent behavior

More importantly, you'll have built a working agent yourself and gained the mental models to build, tune, and debug any agent system you encounter.

## Part 1: What is an AI Agent (and Why Should You Care)?

### The Shift from Models to Agents

Let's start with clarity: **an AI agent is not just an LLM**.

An **LLM** (Large Language Model) is a prediction engine. You give it text, it predicts the next tokens. That's it. Claude, GPT-4, Gemini—they're fundamentally autocomplete on steroids.

An **AI agent** is different. It's a system that:
- **Observes** its environment (reads input, context, tool results)
- **Thinks** about what to do (plans, breaks down tasks)
- **Acts** on the world (calls tools, executes code, searches the web)
- **Reflects** on results (adjusts approach, decides next steps)

The LLM is just the "brain"—the reasoning component. The agent is the complete system that wraps around it.

### A Practical Example

Imagine you ask: *"What are the latest developments in Large Reasoning Models?"*

**LLM alone:** Gives you an answer based on training data (likely outdated, ends at knowledge cutoff).

**Agent with tools:**
1. **Observes:** Recognizes this needs current information
2. **Thinks:** "I need to search the web for recent articles"
3. **Acts:** Searches, reads the top 3-4 sources
4. **Reflects:** "Do I have enough info? Should I search more specific sources?"
5. Returns an up-to-date, cited summary

The agent made decisions, took actions, and orchestrated multiple steps to accomplish the goal. The LLM just provided the reasoning at each step.

### Why This Matters Right Now

#### 1. Agents Are Becoming Infrastructure
GitHub Copilot, Cursor, Claude Code, ChatGPT with plugins—these are all agents. Your IDE is becoming agentic. Your CI/CD pipeline will be agentic. Your monitoring and incident response will be agentic. Understanding how they work isn't optional anymore.

#### 2. The Productivity Multiplier is Real
Teams using agentic development tools are seeing 40-75% reductions in development time for certain tasks. But only when they understand how to prompt them, when to trust them, and when to intervene. Treating them as magic leads to frustration and poor results.

#### 3. Building Custom Agents is Becoming Essential
Off-the-shelf agents won't solve your specific business problems. You'll need to build custom agents for:
- Internal tools and workflows
- Domain-specific research and analysis
- Customer-facing automation
- Development and DevOps tasks

Understanding the fundamentals means you can build these systems confidently instead of cargo-culting frameworks you don't understand.

## The Four-Part Foundation: Observe → Think → Act → Reflect

Before we dive into code, let's establish the core pattern that every agent follows:

### 1. OBSERVE 👁️
**What it means:** The agent gathers information from its environment.
- User input (questions, commands, requests)
- Tool results (web search results, database queries, API responses)
- Context (conversation history, uploaded files, system state)
- Environmental signals (errors, timeouts, success indicators)

**In code:** This is where you receive input and parse it into a format the LLM can understand.

### 2. THINK 🧠
**What it means:** The agent reasons about what to do next using the LLM.
- Analyze the current situation
- Decide if more information is needed
- Determine which tool (if any) to use
- Plan the next step
- Generate responses or commands

**In code:** This is the API call to the LLM, where you send observations and get back reasoning/decisions.

### 3. ACT 🎯
**What it means:** The agent executes actions based on its reasoning.
- Call a function/tool (search web, query database, run code)
- Return an answer to the user
- Modify state or environment
- Trigger workflows

**In code:** This is where you execute the LLM's decision—calling tools, APIs, or returning results.

### 4. REFLECT 🔄
**What it means:** The agent evaluates results and decides what to do next.
- Did the action succeed?
- Is more information needed?
- Should I try a different approach?
- Am I done, or should I loop back to OBSERVE?

**In code:** This is your loop control logic—checking if the task is complete or if another iteration is needed.

This pattern repeats until the agent completes its task or reaches a stopping condition.

## Hands-On: Building Component 1 - The Foundation

Now let's build the foundational piece and see how it maps to our four-part framework.

**What Component 1 teaches:**
- How to connect to an LLM (Gemini API)
- The basic request-response pattern
- How OBSERVE and THINK work in practice
- The foundation for adding ACT and REFLECT later

**Get the code:** [github.com/codenoob1928/learning-agents](https://github.com/codenoob1928/learning-agents)

### Setup (5 minutes)

1. **Get your Gemini API key:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with Google
   - Click "Create API Key"
   - Copy the key

2. **Clone the repository:**
   ```bash
   git clone https://github.com/codenoob1928/learning-agents.git
   cd learning-agents
   pip install -r requirements.txt
   ```

3. **Set your API key:**
   ```bash
   # Windows (PowerShell)
   $env:GOOGLE_API_KEY="your-key-here"
   
   # Windows (CMD)
   set GOOGLE_API_KEY=your-key-here
   
   # Mac/Linux
   export GOOGLE_API_KEY="your-key-here"
   ```

## Breaking Down the Code: Understanding Each Piece

Let's walk through `component_1_basic_connection/basic_connection.py` and connect each part to our four-part foundation.

### Part 1: Setup and Configuration

```python
import os
import google.generativeai as genai

def setup_gemini():
    """Initialize the Gemini API"""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("⚠️  GOOGLE_API_KEY not found!")
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    return model
```

**What's happening here:**
- **Environment reading:** We safely get the API key from environment variables (never hardcode secrets!)
- **API configuration:** We authenticate with Google's servers
- **Model initialization:** We create a model instance ready to receive requests

**Foundation connection:** This is our preparation phase—setting up the infrastructure before we can observe, think, act, or reflect.

**Why this matters:**
- `gemini-1.5-flash` is fast and cost-effective, perfect for agents that make many API calls
- The model object is reusable—create once, use many times
- Error handling here prevents cryptic failures later

### Part 2: The OBSERVE Phase

```python
def ask_question(model, question):
    """
    Send a question to Gemini and get a response
    
    Args:
        model: Initialized Gemini model
        question: User's input (what we're observing)
    """
    print(f"📤 Sending question: {question}\n")
    
    # This is where OBSERVE meets THINK
    response = model.generate_content(question)
    
    return response
```

**What's happening here:**
- **OBSERVE:** We receive the user's question—this is our environmental input
- **Package for processing:** We format it for the LLM to understand
- **Send to LLM:** We hand off to the thinking engine

**Foundation connection:**
- **OBSERVE:** The `question` parameter is what we're observing from the environment (user input)
- **THINK:** The `generate_content()` call triggers the LLM's reasoning process

**Critical insight:** Notice that OBSERVE and THINK happen in the same function here. In Component 1, they're tightly coupled because we have no tools yet. As we add complexity (Components 2-7), you'll see these phases become more distinct.

### Part 3: The THINK Phase (Inside the LLM)

```python
response = model.generate_content(question)
```

**What happens inside this call:**

When you call `generate_content()`, here's what occurs:

1. **Context window preparation:** Your question becomes part of a prompt sent to Gemini
2. **LLM processing:** Gemini's neural network processes the input:
   - Tokenizes the text
   - Runs it through transformer layers
   - Predicts the most likely next tokens
   - Generates a coherent response
3. **Response packaging:** The generated text is wrapped in a response object

**Foundation connection:** This IS the THINK phase.

The LLM is:
- Analyzing your question
- Accessing its training knowledge
- Reasoning about what would be a helpful answer
- Generating a response based on that reasoning

**What you can't see (but should understand):**
- The LLM doesn't "know" anything—it's predicting probable text based on patterns
- It can't access the internet or run code (yet—that's what we'll add in later components)
- It has no memory of previous conversations (we'll fix this in Component 5)

### Part 4: Parsing the Response

```python
def display_response(response):
    """Parse and show the response"""
    print("=" * 70)
    print("📥 GEMINI RESPONSE:")
    print("=" * 70)
    print(response.text)
    print("=" * 70)
    
    # Show metadata
    print(f"\n📊 Metadata:")
    print(f"   Finish reason: {response.candidates[0].finish_reason}")
    print(f"   Safety checks: {len(response.candidates[0].safety_ratings)}")
```

**What's happening here:**
- **Extract the text:** `response.text` gets the actual generated content
- **Examine metadata:** We check how and why the generation stopped
- **Display to user:** We format and present the results

**Foundation connection:** This is where ACT begins.

In Component 1, "acting" is simple—we just return the answer to the user. But this is still an action! The agent is:
- Taking the LLM's reasoning (THINK)
- Extracting the relevant information
- Presenting it to the user (ACT)

**Understanding the response structure:**
```python
response = {
    'text': "The actual generated text",
    'candidates': [
        {
            'finish_reason': 'STOP',  # or 'MAX_TOKENS', 'SAFETY', etc.
            'safety_ratings': [...]    # Content safety checks
        }
    ]
}
```

**Why this matters:**
- `finish_reason` tells you if the response completed naturally or was cut off
- `safety_ratings` shows if content was flagged (important for production)
- Understanding this structure helps you debug when things go wrong

### Part 5: The Main Loop (Simplified Agent Pattern)

```python
def main():
    """Component 1: Basic connection and Q&A"""
    
    # Setup
    model = setup_gemini()
    if not model:
        return
    
    # OBSERVE: Get user input (hardcoded for now)
    question = "Explain what an AI agent is in 2-3 sentences."
    
    # THINK & ACT: Send to LLM and get response
    response = ask_question(model, question)
    
    # ACT: Display the result
    display_response(response)
    
    print("\n✅ Component 1 Complete!")
```

**What's happening here:** This is your first (very simple) agent loop:
1. **Setup:** Initialize the tools we need
2. **OBSERVE:** Get input (hardcoded question for now)
3. **THINK:** Send to LLM for reasoning (`ask_question`)
4. **ACT:** Display the result (`display_response`)
5. **REFLECT:** (Missing in Component 1—we'll add this later)

**Foundation connection - The Complete Flow:**
```
User Question
     ↓
[OBSERVE] - Receive input, understand what's being asked
     ↓
[THINK] - LLM reasons about the question
     ↓
[ACT] - Display the answer
     ↓
[REFLECT] - (Not implemented yet)
     ↓
Done (for now - no loop back)
```

**What's missing (and why):**
- **No loop:** We don't go back to OBSERVE for more input
- **No tools:** We can't search the web or call functions
- **No reflection:** We don't evaluate if we need more information
- **No memory:** Each question is isolated

But that's the point! Component 1 is intentionally simple so you can understand the basic pattern before we add complexity.

## Running Component 1

Let's see it in action:

```bash
cd component_1_basic_connection
python basic_connection.py
```

**Expected output:**
```
======================================================================
COMPONENT 1: Basic Gemini API Connection
======================================================================

✓ Gemini API configured successfully!
✓ Using model: gemini-1.5-flash

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

📊 Metadata:
   Finish reason: STOP
   Safety checks: 4

✅ Component 1 Complete!
```

## Connecting It All: The Four-Part Pattern in Component 1

Let's map exactly where each phase happens in our code:

### OBSERVE Phase
**Where:** `main()` function
```python
question = "Explain what an AI agent is in 2-3 sentences."
```
**What:** We receive input from the environment (in this case, a hardcoded string—later this will be dynamic user input)

### THINK Phase
**Where:** Inside `model.generate_content()`
```python
response = model.generate_content(question)
```
**What:** The LLM processes the observation and reasons about the best response

### ACT Phase
**Where:** `display_response()` function
```python
print(response.text)
```
**What:** We take action based on the LLM's reasoning (displaying the answer to the user)

### REFLECT Phase
**Where:** Not implemented in Component 1
**Why:** We'll add this in Component 3 when we introduce the agent loop
**What it will do:** Evaluate if we need more information, if the task is complete, or if we should try a different approach

## What You Just Learned

### 1. The Request-Response Pattern
Every agent interaction fundamentally relies on this:
```python
response = model.generate_content(input)
```
This is the foundation. Everything builds on this.

### 2. The Four-Part Pattern (Simplified)
Even in this simple example, you can see:
- **Observe:** Getting user input
- **Think:** LLM processing
- **Act:** Returning results
- **Reflect:** (Coming in later components)

### 3. Response Structure
Understanding what comes back from the LLM:
- `text`: The generated content
- `finish_reason`: Why it stopped
- `safety_ratings`: Content checks

### 4. Why Start Simple
Component 1 intentionally leaves out:
- Tool calling (Component 2)
- Looping/iteration (Component 3)
- Planning (Component 4)
- Memory (Component 5)
- Error handling (Component 6)

Each component adds ONE new concept on top of this foundation.

## Key Insights for Building Agents

### 1. Agents are systems, not just LLM calls
The LLM is just the reasoning engine. An agent is:
- Input handling (OBSERVE)
- LLM reasoning (THINK)
- Tool execution (ACT)
- Evaluation logic (REFLECT)
- Loop control (deciding to continue or stop)

### 2. The pattern scales
This same observe-think-act-reflect pattern works for:
- Simple Q&A (Component 1)
- Tool-using agents (Components 2-3)
- Planning agents (Component 4)
- Multi-agent systems (beyond this series)

### 3. Start with the fundamentals
Understanding this basic pattern makes everything else easier. When your production agent fails, you can trace it back to: "Which phase failed? Observe? Think? Act? Reflect?"

## Your Homework Before Part 2

### 1. Get Component 1 working
Actually run the code. Don't just read—execute it.

### 2. Experiment
Try different questions:
- Very short questions
- Complex, multi-part questions
- Questions in different languages
- Questions that require math or reasoning

See how the LLM responds. This builds intuition.

### 3. Break it
Try to make it fail:
- Empty string
- Extremely long input
- Remove the API key
- Set an invalid model name

Understanding failure modes is crucial.

### 4. Think ahead
If you wanted this agent to search the web when it doesn't know something, what would you need to add? Where in the code would it go?

Think through:
- How would the agent know it needs to search?
- What would the search function look like?
- How would you integrate the search results back into the response?

We'll answer these questions in Component 2.

## What's Next: The Learning Path

Each component adds ONE new concept:

**Component 2: Single Tool Calling** (Next post)
- Add a `search_web()` function
- Teach the agent when to use it
- See the agent make its first autonomous decision
- **New phases:** ACT becomes more complex (tool execution)

**Component 3: The Agent Loop**
- Multi-step reasoning
- Chain multiple tool calls
- Complete complex tasks
- **New phases:** REFLECT implemented (loop control)

**Component 4: Planning & Reasoning**
- Break down complex questions into subtasks
- Show the agent's thinking process
- Chain-of-thought prompting
- **New phases:** Enhanced THINK (strategic planning)

**Component 5: Memory & Context**
- Remember across conversations
- Manage context window
- Session state
- **New phases:** Enhanced OBSERVE (historical context)

**Component 6: Error Handling**
- Graceful failures
- Retry logic
- Production readiness
- **New phases:** Enhanced REFLECT (error recovery)

**Component 7: Full Research Agent**
- Multiple specialized tools
- Tool orchestration
- End-to-end automation
- **All phases:** Working together in production

## Why This Approach Works

### 1. Incremental complexity
Each component is understandable on its own. You build intuition step by step.

### 2. Runnable at every stage
Every component produces visible results. You're never "waiting until the end" to see it work.

### 3. Conceptual framework first
The observe-think-act-reflect pattern gives you a mental model. Every new feature maps back to these four phases.

### 4. Real code, real understanding
No hand-waving, no "magic happens here." Every line is explained and mapped to concepts.

## Join the Journey

In Part 2, we'll add our first tool and watch the agent make its first real decision—choosing when to search the web versus answering from its knowledge.

That's when the four-part pattern really comes alive:
- **OBSERVE:** User question + tool results
- **THINK:** "Do I know this? Or should I search?"
- **ACT:** Execute search OR return answer
- **REFLECT:** "Was the search sufficient? Do I need more?"

This is where agents become more than chatbots.

**Questions? Thoughts? Stuck on something?**
Open an issue on [GitHub](https://github.com/codenoob1928/learning-agents) and let's discuss. This is a learning journey we're taking together.

**Code Repository:** [github.com/codenoob1928/learning-agents](https://github.com/codenoob1928/learning-agents)

## Coming in Part 2:
- Function calling / tool use
- Teaching the agent when to use tools
- Structured outputs
- Your first agentic decision
- The ACT phase gets interesting

Until then, get Component 1 working and start thinking about how you'd add a search capability. See you in the next post! 🚀

---

## Series Links:
- **Part 1: What is an Agent?** (You are here)
- **Part 2: Tool Calling** (Coming soon)
- **Part 3: The Agent Loop** (Coming soon)
- **Part 4: Planning & Reasoning** (Coming soon)
- **Part 5: Memory & Context** (Coming soon)
- **Part 6: Error Handling** (Coming soon)
- **Part 7: Full Research Agent** (Coming soon)

**Tags:** #AI #Agents #MachineLearning #Python #Gemini #LLM #Development #ObserveThinkActReflect