# 🧠 DocBridge-MCP — Debugging Assistant Powered by Claude MCP

> An AI-driven debugging assistant built using **Model Context Protocol (MCP)** that integrates directly with **Claude Desktop**, helping developers query documentation, analyze issues, and accelerate debugging workflows.

---

## 1. 🧩 Problem Statement

According to recent industry surveys, **developers spend over 40% of their time debugging or searching for documentation** instead of shipping features. This lost productivity translates to significant delays in software delivery and increased frustration among development teams.

**The Challenge:**
- Manual documentation searches are time-consuming and fragmented
- Debugging workflows require constant context-switching between IDE and browser
- Most debugging assistants rely on generic search without understanding your specific codebase

**DocBridge-MCP solves this** by bringing instant, AI-powered documentation lookup directly into Claude Desktop — your conversational coding partner.

---

## 2. 💡 Motivation

The motivation behind DocBridge-MCP was to bridge the gap between developers and documentation by:

- **Building a local MCP server** that connects seamlessly to Claude Desktop without external API overhead
- **Enabling Claude to fetch documentation dynamically** through custom tool calls, maintaining context across your conversation
- **Creating a foundation for self-debugging agents** that can analyze logs, tracebacks, and errors autonomously in future iterations
- **Reducing context-switching** by keeping developers in their IDE assistant flow

This project demonstrates how MCP servers can extend Claude's capabilities with domain-specific tools tailored for developer workflows.

---

## 3. ⚙️ Tools and Tech Stack Used

| Component | Purpose | Installation/Key |
|-----------|---------|------------------|
| **Claude Desktop** | Primary conversational interface for debugging | [Download](https://claude.ai/download) |
| **Model Context Protocol (MCP)** | Framework for extending Claude with local tools | [Docs](https://modelcontextprotocol.io/) |
| **Python 3.10+** | Backend server logic and tool execution | [Download](https://www.python.org/downloads/) |
| **Groq API** | Fast LLM inference for processing queries | [Get Free API Key](https://console.groq.com/keys) |
| **Serper API** | Documentation search and web scraping | [Get Free API Key](https://serper.dev/) |

### Getting API Keys

**Groq API Key:**
1. Visit [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up with Google or email
3. Click "Create API Key"
4. Copy the key and save it securely

**Serper API Key:**
1. Visit [https://serper.dev/](https://serper.dev/)
2. Sign up for free (includes 100 free searches)
3. Go to API Key section in dashboard
4. Copy your API key

---

## 4. 🚀 How to Run This Project

### Prerequisites

- Python 3.10 or higher
- Claude Desktop installed
- Valid Groq and Serper API keys

### Installation & Setup

#### **Option A: Using `uv` (Recommended - Faster)**

**Step 1: Install `uv` package manager**

```bash
pip install uv
```

**Step 2: Clone and setup on Windows**

```bash
git clone https://github.com/Vibhuarvind/DocBridge-MCP.git
cd DocBridge-MCP
uv venv .venv
.venv\Scripts\activate
uv sync
```

**Step 2: Clone and setup on macOS/Linux**

```bash
git clone https://github.com/Vibhuarvind/DocBridge-MCP.git
cd DocBridge-MCP
uv venv .venv
source .venv/bin/activate
uv sync
```

#### **Option B: Using `pip` (Traditional)**

**Step 1: Clone and setup on Windows**

```bash
git clone https://github.com/Vibhuarvind/DocBridge-MCP.git
cd DocBridge-MCP
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

**Step 1: Clone and setup on macOS/Linux**

```bash
git clone https://github.com/Vibhuarvind/DocBridge-MCP.git
cd DocBridge-MCP
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Tip:** `uv` is 10-100x faster and handles dependency resolution better. Highly recommended!

### Environment Variables

Create a `.env` file in your project root:

```bash
SERPER_API_KEY=your-serper-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

Or export them directly:

**Windows (PowerShell):**

```powershell
$env:SERPER_API_KEY="your-serper-api-key-here"
$env:GROQ_API_KEY="your-groq-api-key-here"
```

**macOS/Linux (Bash/Zsh):**

```bash
export SERPER_API_KEY="your-serper-api-key-here"
export GROQ_API_KEY="your-groq-api-key-here"
```

### Running the Server

**On Windows:**

```bash
python mcp_server.py
```

**On macOS/Linux:**

```bash
python3 mcp_server.py
```

You should see output like:

```
[INFO] MCP Server initialized
[INFO] Tool 'get_docs' registered successfully
[INFO] Server listening on stdio transport
```

### Debug Logs

All logs are automatically created in the `logs/` directory:

```
logs/
├── mcp_server.log          # Main server logs
├── tool_calls.log          # Tool invocation traces
└── api_responses.log       # API response data
```

Monitor logs in real-time:

**Windows:**

```bash
Get-Content logs/mcp_server.log -Wait
```

**macOS/Linux:**

```bash
tail -f logs/mcp_server.log
```

---

## 5. 🧪 Debugging & Claude Setup

### Step 1: Configure MCP Server in Claude Desktop

1. Open **Claude Desktop**
2. Go to **Settings → Developer → Local MCP Servers**
3. Click **Edit Config** (opens the config file)
4. Add this JSON configuration:

**For Windows:**

```json
{
    "mcpServers": {
        "docs-mcp": {
            "command": "C:\\Users\\YourUsername\\DocBridge-MCP\\.venv\\Scripts\\python.exe",
            "args": ["C:\\Users\\YourUsername\\DocBridge-MCP\\mcp_server.py"],
            "cwd": "C:\\Users\\YourUsername\\DocBridge-MCP",
            "env": {
                "SERPER_API_KEY": "your-serper-api-key-here",
                "GROQ_API_KEY": "your-groq-api-key-here"
            }
        }
    }
}
```

**For macOS/Linux:**

```json
{
    "mcpServers": {
        "docs-mcp": {
            "command": "/Users/your-username/DocBridge-MCP/.venv/bin/python",
            "args": ["/Users/your-username/DocBridge-MCP/mcp_server.py"],
            "cwd": "/Users/your-username/DocBridge-MCP",
            "env": {
                "SERPER_API_KEY": "your-serper-api-key-here",
                "GROQ_API_KEY": "your-groq-api-key-here"
            }
        }
    }
}
```

5. Save the file and **restart Claude Desktop**
6. You should see `docs-mcp — running ✅` in the status indicator

### Step 2: Understanding Tool Calling

Once configured, Claude will automatically detect your MCP tool. You can invoke it naturally in conversations:

**Available Tool:**

```
get_docs(query: string) — Fetches relevant documentation based on your query
```

Claude will call this tool when you ask questions about documentation or debugging issues. The tool returns structured documentation snippets, links, and code examples.

### Step 3: Toy Example Prompts

#### ✅ **Positive Scenario: Documentation Found**

**Your Prompt:**

```
Use get_docs to find how to connect LangChain with ChromaDB for vector storage.
```

**Expected Output:**

```
Found relevant documentation on LangChain-ChromaDB integration:

1. Installation:
   pip install langchain chroma-db

2. Basic Setup:
   from langchain.vectorstores import Chroma
   from langchain.embeddings import OpenAIEmbeddings
   
   embeddings = OpenAIEmbeddings()
   vectorstore = Chroma.from_documents(
       documents=docs,
       embedding=embeddings
   )

3. Reference Links:
   - https://python.langchain.com/docs/integrations/vectorstores/chroma
   - https://docs.trychroma.com/

The tool successfully retrieves documentation and Claude explains how to integrate
these two libraries for your vector database needs.
```

---

#### ❌ **Negative Scenario: Documentation Not Found**

**Your Prompt:**

```
Use get_docs to find recipes for baking chocolate chip cookies.
```

**Expected Output:**

```
I don't have relevant technical documentation for that query.

DocBridge-MCP is designed for software development and debugging topics.
Please try queries like:
- "How to set up Docker containers"
- "FastAPI database connection patterns"
- "Python async/await best practices"

This validates that your tool properly filters non-technical queries and
provides helpful guidance when documentation isn't available.
```

---

### Step 4: Using MCP Inspector for Debugging

The MCP Inspector is a powerful tool for visualizing and debugging MCP server communications. It shows you exactly what Claude is sending to your server and what responses are returned.

**Install and run MCP Inspector:**

```bash
npx @modelcontextprotocol/inspector
```

This opens an interactive web interface where you can:

**Features of MCP Inspector:**

- **View live requests** — See JSON payloads that Claude sends to your MCP server
- **Inspect responses** — View your server's responses in real-time
- **Debug tool calls** — Trace tool invocation parameters and return values
- **Monitor performance** — Check API response times and bottlenecks
- **Test tools manually** — Invoke tools directly without Claude to test them
- **Catch errors** — See malformed responses, timeouts, and exceptions immediately

**Why Use It:**

1. **Debugging Integration Issues** — If Claude isn't calling your tool, MCP Inspector shows why
2. **Performance Monitoring** — Identify slow API calls or data processing bottlenecks
3. **Response Validation** — Ensure your tool returns properly formatted JSON
4. **Development Workflow** — Faster iteration during MCP server development
5. **Error Tracking** — Catch and fix issues before they reach Claude

**Example: Debugging a Failed Tool Call**

If you ask Claude to use `get_docs` but it fails, MCP Inspector shows:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_docs",
    "arguments": {
      "query": "Python async patterns"
    }
  }
}
```

And the response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found documentation on async patterns..."
      }
    ]
  }
}
```

---

## 6. 🚀 Future Enhancements

### AI-Enabled HTML Scraping Strategy

Currently, documentation scraping is static. The vision is to make it intelligent:

**The Concept:**

```python
# Instead of manual parsing:
raw_html = fetch_documentation_page(url)
relevant_content = parse_html_with_regex(raw_html)  # Brittle & limited

# Use AI-powered extraction:
raw_html = fetch_documentation_page(url)
response = llm_function(f"Extract setup instructions from: {raw_html}")
relevant_content = response.text
```

**Handling Bloated Responses:**

When the LLM returns verbose HTML parsing results, use chunking strategy:

```python
def chunk_response(response_text, chunk_size=500):
    """Split long responses into manageable chunks"""
    chunks = [
        response_text[i:i+chunk_size] 
        for i in range(0, len(response_text), chunk_size)
    ]
    return chunks

# Process each chunk for relevance scoring
for chunk in chunks:
    relevance_score = score_chunk_relevance(chunk, user_query)
    if relevance_score > threshold:
        use_chunk_in_response(chunk)
```

This ensures:
- AI extracts only relevant sections from bloated HTML
- Chunking strategy handles memory limitations
- Relevance scoring prioritizes useful information
- Users get concise, actionable answers

### Planned Features

- **Async API Requests** — Handle multiple documentation queries simultaneously without blocking
- **Smart Caching** — Store frequently accessed docs for instant retrieval
- **Code Analysis** — Analyze error tracebacks and suggest fixes automatically
- **Multi-Agent Debugging** — Use LangGraph to orchestrate multiple specialized debugging agents
- **Custom Documentation Sources** — Allow users to register their own documentation URLs
- **Conversation Memory** — Maintain context across debugging sessions

### Production Ready Release (Coming Soon)

The next release will include:

- Full async/await implementation for concurrent requests
- Comprehensive config validation before server startup
- Environment variable schema checking
- Multi-agent orchestration framework using LangGraph
- Unit tests and integration tests
- Docker containerization for easy deployment
- Performance benchmarks and optimization

---

## 7. 📚 Sources & References

This project was built on the foundations of:

- **MCP Documentation:** [https://modelcontextprotocol.io/docs/develop/build-server](https://modelcontextprotocol.io/docs/develop/build-server) — Core protocol specifications and tool building patterns
- **MCP Weather API Example:** [https://modelcontextprotocol.io/docs/develop/build-server#weather-api-issues](https://modelcontextprotocol.io/docs/develop/build-server#weather-api-issues) — Reference implementation for understanding tool response structures
- **Claude Desktop Setup:** [https://claude.ai/docs](https://claude.ai/docs) — Integration guidelines and best practices
- **Software Debugging Standards:** Added to `debug.py` for standardized error handling, response logging, and debugging workflows following industry best practices

### Key Learning Resources

- Anthropic's Model Context Protocol specification
- Software engineering debugging methodologies
- API integration patterns and error handling
- Async Python patterns for concurrent operations

---

## 📁 Project Structure

```
DocBridge-MCP/
├── mcp_server.py              # Main MCP server with tool registration
├── debug.py                   # Standardized debugging & logging utilities
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Git ignore rules
├── logs/                      # Debug logs (auto-generated)
│   ├── mcp_server.log
│   ├── tool_calls.log
│   └── api_responses.log
└── README.md                  # This file
```

---

## 🔧 Troubleshooting

### Issue: "docs-mcp — error ❌"

**Solution:** Verify paths in Claude Desktop config use absolute paths (not relative):

```json
"command": "C:\\Users\\YourName\\DocBridge-MCP\\.venv\\Scripts\\python.exe"
```

Check logs:

```bash
tail -f logs/mcp_server.log
```

### Issue: API Key Errors

**Solution:** Verify keys are set:

```bash
# Windows
echo %SERPER_API_KEY%
echo %GROQ_API_KEY%

# macOS/Linux
echo $SERPER_API_KEY
echo $GROQ_API_KEY
```

Both should print your keys. If blank, set them in `.env` or environment.

### Issue: Tool Not Invoked

**Solution:** After updating config, restart Claude Desktop completely. Check MCP Inspector for errors:

```bash
npx @modelcontextprotocol/inspector
```

### Issue: Slow Responses

**Solution:** Monitor API response times in `logs/api_responses.log`. Consider:
- Checking Groq/Serper API status
- Reducing query complexity
- Enabling caching for repeated queries

---

## ✨ Author

**Vidisha Arvind**  
*M.Tech in Data Science | AI Enthusiast | Building AI-assisted developer tools*

---

## 📄 License

This project is open source. See `LICENSE` file for details.

---

## 💬 Feedback & Contributions

Found a bug? Have a feature idea? Open an issue or submit a pull request on GitHub!

**Repository:** [https://github.com/Vibhuarvind/DocBridge-MCP](https://github.com/Vibhuarvind/DocBridge-MCP)
