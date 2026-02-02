# MCP Claude - Document Management CLI

A powerful command-line interface application that integrates **Model Context Protocol (MCP)** with **Claude AI** for intelligent document management, formatting, and summarization.

## 🎯 Overview

MCP Claude is a Python-based CLI tool that demonstrates how to build AI-powered document workflows using the Model Context Protocol. It provides a conversational interface where users can interact with documents, apply AI-driven formatting, and generate summaries—all through natural language commands.

## ✨ Features

### MCP Server Capabilities

| Feature | Description |
|---------|-------------|
| **Tools** | `read_doc_content` - Read document contents<br>`edit_doc_content` - Edit documents with find/replace |
| **Resources** | `docs://documents` - List all document IDs<br>`docs://documents/{doc_id}` - Fetch specific document content |
| **Prompts** | `/format` - Convert documents to well-structured Markdown<br>`/summarize` - Generate concise document summaries |

### CLI Features

- 💬 **Interactive Chat** - Natural language conversation with Claude AI
- 📄 **Document Mentions** - Reference documents using `@document.ext` syntax
- 🔧 **Tool Integration** - AI automatically uses available tools to complete tasks
- 🔄 **Multi-Client Support** - Connect multiple MCP servers simultaneously

## 🏗️ Architecture

```
mcp_claude_1/
├── main.py              # Application entry point
├── mcp_server.py        # MCP server with tools, resources, and prompts
├── mcp_client.py        # MCP client wrapper for server communication
├── core/
│   ├── chat.py          # Base chat functionality
│   ├── cli_chat.py      # CLI-specific chat implementation
│   ├── cli.py           # CLI application UI
│   ├── claude.py        # Anthropic Claude API wrapper
│   └── tools.py         # Tool execution manager
├── pyproject.toml       # Project configuration
└── .env                 # Environment variables (API keys)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Anthropic API key
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

---

### 🟢 Option 1: Using uv (Recommended)

[uv](https://docs.astral.sh/uv/) is an extremely fast Python package and project manager written in Rust. It handles virtual environments and dependencies automatically, making setup straightforward.

#### Step 1: Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via Homebrew (macOS)
brew install uv
```

#### Step 2: Clone the Repository

```bash
git clone https://github.com/mattsebastianh/mcp_claude_1.git
cd mcp_claude_1
```

#### Step 3: Install Dependencies

```bash
# uv automatically creates .venv and installs all dependencies
uv sync
```

> **Note:** `uv sync` reads `pyproject.toml` and `uv.lock` to install exact dependency versions, ensuring reproducible builds.

#### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
CLAUDE_MODEL="claude-sonnet-4-5"
ANTHROPIC_API_KEY="<YOUR-CLAUDE-API-KEY>"

# Set to 1 when using uv
USE_UV=1
```

#### Step 5: Run the Application

```bash
# uv run automatically uses the project's virtual environment
uv run python main.py
```

**Why use uv?**
- ⚡ 10-100x faster than pip
- 🔒 Lock file support (`uv.lock`) for reproducible builds
- 🎯 Automatic virtual environment management
- 📦 Built-in dependency resolver

---

### 🔵 Option 2: Using pip (Alternative)

Traditional Python setup using pip and venv.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/mattsebastianh/mcp_claude_1.git
cd mcp_claude_1
```

#### Step 2: Create Virtual Environment

```bash
python3 -m venv .venv
```

#### Step 3: Activate Virtual Environment

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

#### Step 4: Install Dependencies

```bash
pip install -r requirements.txt

# Or install in editable mode for development
pip install -e .
```

#### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
CLAUDE_MODEL="claude-sonnet-4-5"
ANTHROPIC_API_KEY="<YOUR-CLAUDE-API-KEY>"

# Set to 0 when using pip
USE_UV=0
```

#### Step 6: Run the Application

```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # macOS/Linux

# Run the application
python main.py
```

---

## 📖 Usage

### Interactive Commands

Once the CLI is running, you can interact with documents:

```
> What documents are available?
> @report.pdf What does this report cover?
> /format deposition.md
> /summarize financials.docx
```

### Document Mentions

Reference documents directly in your queries using the `@` prefix:

```
> Compare @report.pdf with @outlook.pdf
> Summarize the key points from @deposition.md
```

### Prompt Commands

Use slash commands to trigger specific AI workflows:

| Command | Usage | Description |
|---------|-------|-------------|
| `/format` | `/format <doc_id>` | Convert document to structured Markdown |
| `/summarize` | `/summarize <doc_id>` | Generate a concise 3-5 sentence summary |

## 🔧 MCP Server Details

### Tools

#### `read_doc_content`
Reads and returns the content of a document.
```python
# Input
{"doc_id": "report.pdf"}

# Output
"The report details the state of a 20m condenser tower."
```

#### `edit_doc_content`
Edits document content by replacing strings.
```python
# Input
{
    "doc_id": "report.pdf",
    "old_strings": ["20m"],
    "new_strings": ["25m"]
}
```

### Resources

- **`docs://documents`** - Returns a JSON array of all document IDs
- **`docs://documents/{doc_id}`** - Returns the plain text content of a specific document

### Prompts

The MCP server exposes prompts that provide structured instructions to the AI:

- **`format`** - Guides the AI to reformat documents into clean Markdown with proper headers, lists, and tables
- **`summarize`** - Instructs the AI to extract key points and create concise summaries

## 🧪 Testing with MCP Inspector

Test your MCP server implementation using the MCP Inspector:

```bash
# Using uv (recommended)
npx @modelcontextprotocol/inspector uv run python mcp_server.py

# Using pip/venv (make sure .venv is activated)
npx @modelcontextprotocol/inspector .venv/bin/python mcp_server.py
```

This opens a web interface at `http://localhost:6274` where you can:
- View available tools, resources, and prompts
- Test tool calls with different inputs
- Debug server responses

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `anthropic` | Claude AI API client |
| `mcp[cli]` | Model Context Protocol SDK |
| `fastmcp` | FastMCP server framework |
| `prompt-toolkit` | Interactive CLI interface |
| `python-dotenv` | Environment variable management |

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `CLAUDE_MODEL` | Yes | Claude model to use (e.g., `claude-sonnet-4-5`) |
| `USE_UV` | No | Set to `1` for uv, `0` for pip (default: `0`) |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [uv - Python Package Manager](https://docs.astral.sh/uv/)
