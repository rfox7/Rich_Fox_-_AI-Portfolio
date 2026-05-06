# Lab 10 — Building Agents with Frameworks (Tools, Memory, Workflow)

> **Course:** Applied AI — Computer Vision (ITAI 1378)
> **Module:** 10 (Capstone)
> **Type:** Lab / Hands-on Exercise + Reflection
> **Student:** Rich Fox
> **File:** `L10_Fox_Rich_ITAI1378.ipynb`

---

## Overview

In this capstone lab, we scaled beyond the perception-action loop of Lab 9 to build **agent frameworks** — structured systems where agents compose multiple tools to accomplish complex tasks. Using a simple weather/population agent as the base, we learned how frameworks decouple tools (functions), workflows (decision logic), and memory (state management). The student challenge extended the agent with a new tool for fun facts, illustrating how frameworks enable extensibility without redesigning the core agent.

---

## What I Learned

- **Agent frameworks separate concerns.** Tools, workflow, and memory are distinct. This separation enables building complex agents by combining simple, reusable components — the essence of good software architecture.

- **Tools are the agent's API to the world.** Whether calling a weather API, a calculator, a database, or another AI model, tools define what actions the agent can take. The workflow (decision logic) chooses which tool to invoke.

- **Workflow is the agent's decision-making engine.** In our simple agent, it was keyword-based if-then logic. In production frameworks like LangChain, it's an LLM that reasons about which tool fits the task. This is the critical difference between rigid and flexible agents.

- **Memory enables learning and context.** Our agent had no memory — it forgot every conversation. Real agents maintain short-term context (last few turns) and long-term knowledge (stored facts). Memory transforms agents from stateless functions into persistent assistants.

- **Extensibility requires clean abstractions.** Adding the `get_fun_fact()` tool required minimal changes to the workflow — just a new elif branch. Good frameworks make adding tools trivial, not painful.

- **Real frameworks trade simplicity for power.** Keyword-based routing is predictable and debuggable. LLM-based routing is flexible but less interpretable, hallucination-prone, and more expensive. The choice reflects your application's needs.

---

## Challenges Faced

The main challenge was **recognizing what the framework provided vs. what we were building ourselves**. The lab deliberately simplified the framework (just Python functions and if-else logic) to teach core concepts. Real frameworks like LangChain abstract much more:

- **Tool discovery:** How does the agent know what tools exist?
- **Tool selection:** How does it pick the right one given a query?
- **Tool chaining:** What if one tool's output feeds into another?
- **Error handling:** What happens if a tool fails?
- **Memory management:** How much to store? What to forget?

Our simple agent required manual keyword extraction ("Boston" in prompt) and hardcoded if-elif chains. A production framework handles this dynamically. Understanding this gap clarified why frameworks exist.

---

## Architecture: Tools, Memory, Workflow

### 1. Tools

**Definition:** Functions or services the agent can call to accomplish tasks.

```python
def get_weather(city):
    """A tool that returns the weather for a given city."""
    if city == "Boston":
        return "The weather in Boston is 70 degrees and sunny."
    # ...
```

**In production:**
- Web search API
- Database queries
- Calculator for math
- Another AI model (text generation, summarization)
- Real-time data (stock prices, weather API)
- File system operations

**Key insight:** Tools should have clear inputs/outputs and single responsibilities.

---

### 2. Memory

**Definition:** Storage of past interactions, learned facts, and context.

**Types:**
- **Short-term (Buffer):** Last N messages or interactions
- **Long-term (Retrieval):** Stored facts; queried via search
- **Episodic:** Memories of specific events

**In our agent:** None. Each query started fresh.

**In production systems:**
- Conversation history (context for follow-up questions)
- User profiles (preferences, history)
- Knowledge base (facts about the domain)
- Learned patterns (what worked before)

---

### 3. Workflow

**Definition:** Logic that routes queries to tools and orchestrates responses.

```python
def weather_agent(prompt):
    if "weather" in prompt:
        # Extract city, call get_weather tool
    elif "population" in prompt:
        # Extract city, call get_population tool
    else:
        # Default response
```

**Levels of sophistication:**

| Level | Method | Pros | Cons |
|---|---|---|---|
| **1. Hardcoded** | If-elif-else on keywords | Predictable, debuggable | Brittle, not scalable |
| **2. Pattern matching** | Regex, NLP tokenization | More flexible | Still limited to patterns |
| **3. Rule-based** | Expert systems (CLIPS, Prolog) | Can express complex logic | Requires manual rules |
| **4. LLM-based** | "Think, decide which tool, execute" | Highly flexible, natural language | Unpredictable, expensive |

Our lab used **Level 1**. Production systems typically use **Level 3 or 4**.

---

## Student Challenge: Extending the Agent

**Task:** Add a new tool (`get_fun_fact()`) and integrate it into the workflow.

**Implementation:**

```python
def get_fun_fact(city):
    """A tool that returns a fun fact for a given city."""
    if city == "Boston":
        return "Boston got its nickname 'Beantown' because of the baked beans..."
    elif city == "San Francisco":
        return "San Francisco contains more dogs than children..."
```

**Workflow update:** Added an elif branch checking for "fact" keyword.

**Key observation:** Adding a new capability required:
1. Define the tool (function)
2. Add a branch to the workflow
3. Test the integration

**In a good framework:** Just register the tool; the framework handles routing.

---

## Reflection Insights

### Agentic Concepts (Q1)

**Tools:** The `get_weather()`, `get_population()`, `get_fun_fact()` functions that perform actions.

**Workflow:** The if-elif-else logic in `weather_agent()` and `extended_weather_agent()` that decides which tool to use.

**Memory:** None. The agent doesn't retain information between calls. Each query is independent.

**Why no memory?** The lab intentionally simplified. Production agents need memory for context, learning, and personalization.

---

### Why Frameworks Matter (Q2)

**Without a framework:**
- Hardcode logic for each new capability
- Duplicate routing logic across agents
- Manual error handling and retries
- No standard way to compose tools
- Difficult to test and debug

**With a framework:**
- Register tools once; routing is automatic
- Reusable workflows across agents
- Built-in error handling, logging, caching
- Composable tool chains
- Clear abstractions for testing

**Example:** Adding a new tool in LangChain requires ~3 lines. In our simple agent, it required modifying the workflow function.

---

### Customer Service Agent Tools (Q3)

For an online store, three essential tools:

1. **Customer Information Tool**
   - Retrieve account details, order history
   - Update preferences, contact info
   - Use case: "What's my account email?"

2. **Product Information Tool**
   - Check inventory, specs, pricing
   - Search by name/category/rating
   - Use case: "Is the blue shirt in size M available?"

3. **Payment/Billing Tool**
   - Process refunds, track payments
   - Dispute resolution
   - Use case: "I was charged twice; can you refund?"

**Advanced tools to consider:**
- Return processing (print label, track status)
- Chat history (context for follow-up questions)
- Recommendation engine (suggest related products)

---

### LLM-Based Routing vs. Rule-Based (Q4)

**Rule-based (keyword matching):**

| Pros | Cons |
|---|---|
| Predictable, debuggable | Brittle to paraphrasing ("What's the climate in Boston?") |
| Fast, cheap | Labor-intensive to maintain rules |
| Clear error handling | Doesn't scale to many tools |

**LLM-based:**

| Pros | Cons |
|---|---|
| Flexible, handles natural language | Less predictable, harder to debug |
| Automatically scales to many tools | Hallucinations ("tool that doesn't exist") |
| Enables complex reasoning | More expensive (API calls) |
| Maintains conversation context | Slower (LLM inference time) |

**Best practice:** Hybrid — use LLM for complex queries, rules for simple/frequent ones.

---

## Real-World Agent Frameworks

| Framework | Language | Strengths | Use Case |
|---|---|---|---|
| **LangChain** | Python/JS | Flexible, many integrations | Custom agents, RAG systems |
| **LlamaIndex** | Python | Document indexing, retrieval | Q&A over documents |
| **AutoGen** | Python | Multi-agent conversation | Complex workflows |
| **Semantic Kernel** | C#/Python | LLM orchestration | Enterprise integration |
| **CrewAI** | Python | Team-based agents | Collaborative tasks |

---

## From Labs 9 → 10: The Evolution

**Lab 9 (Perception-Reasoning-Action):**
- Single loop: detect → decide → act
- Fixed output (print alert)
- No memory or tool abstraction
- Example: YOLO-based security monitor

**Lab 10 (Frameworks):**
- Multiple tools available
- Dynamic tool selection based on query
- Extensible without redesign
- Memory for context
- Example: Customer service bot with weather/population/facts

**Next frontier:**
- Multi-agent collaboration (agents calling other agents)
- Hierarchical reasoning (breaking complex tasks into subtasks)
- Learned policies (agents improving through feedback)

---

## Building a Production Agent

### Phase 1: Simple Rule-Based
Start with hardcoded logic (like our lab). Understand the domain first.

### Phase 2: Tool Abstraction
Decouple tools from workflow. Use a simple framework.

### Phase 3: LLM-Based Routing
Introduce an LLM to decide which tools to use. Handle failures gracefully.

### Phase 4: Memory Integration
Add context windows, long-term storage, and retrieval augmented generation (RAG).

### Phase 5: Multi-Agent
Multiple agents with different specialties collaborating on complex tasks.

---

## Ethical Considerations for Agent Frameworks

1. **Transparency:** Users should know they're interacting with an agent, not a human.

2. **Limitations:** Clearly communicate what the agent can/can't do.

3. **Escalation:** Provide clear paths to human support for complex issues.

4. **Tool trust:** Ensure tools are reliable and don't have unintended side effects.

5. **Memory privacy:** How long is conversation history stored? Who has access?

6. **Hallucinations:** LLM-based agents can invent plausible but false information. Validate outputs.

7. **Fairness:** If tools incorporate biased data (user history, recommendations), agents inherit the bias.

---

## Technologies Used

| Component | Purpose |
|---|---|
| Python | Pure Python for simplicity; no external frameworks |
| Function definitions | Tool implementation |
| If-elif-else logic | Workflow routing |

In production: LangChain, LlamaIndex, or similar frameworks.

---

## How to Run

```bash
cd "Computer Vision/Labs/Lab10"
jupyter notebook L10_Fox_Rich_ITAI1378.ipynb
```

1. Run cells to understand base agent architecture
2. Complete student challenge: add `get_fun_fact()` tool
3. Extend workflow to route fact queries
4. Test with sample prompts
5. Answer reflection questions

---

## Summary: The Full 10-Lab Journey

| Lab | Focus | Key Concept |
|---|---|---|
| **Lab 1** | Image processing | Pixels as data |
| **Lab 2** | Classical features | Engineered representations |
| **Lab 3** | Classical vs. Deep ML | Trade-offs |
| **Lab 4–5** | Deep CNNs | Learned representations |
| **Lab 6** | Object detection | Localization + classification |
| **Lab 7–8** | Multimodal learning | Vision + language |
| **Lab 9** | Perception-Reasoning-Action | Simple agents |
| **Lab 10** | Agent frameworks | Tools, workflows, memory |

**Trajectory:** From analyzing pixels → building perception systems → understanding scenes → reasoning across modalities → **building autonomous agents that solve real problems.**

---

## Key Takeaway

Lab 10 is about **abstraction and composition**. An agent framework isn't magic — it's a well-designed structure that separates tools (what the agent can do) from workflow (when to do it) from memory (what it remembers). 

This separation of concerns scales from simple rule-based systems (Labs 1-9) to sophisticated AI assistants. As you move into real-world deployments, you'll constantly make trade-offs:
- Simplicity vs. flexibility
- Predictability vs. capability
- Cost vs. reliability
- Speed vs. accuracy

Frameworks exist to manage these trade-offs systematically. Your job is understanding the fundamental concepts (tools, workflow, memory), then choosing the right framework and tooling for your specific problem.

The future of AI isn't about building bigger models — it's about composing them intelligently into systems that solve real problems, maintain human oversight, and respect ethical boundaries.

---

*[← Back to Computer Vision](../../README.md) | [← Back to Portfolio Home](../../../README.md)*
