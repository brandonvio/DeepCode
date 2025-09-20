# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DeepCode is an AI Research Engine that transforms research papers and natural language descriptions into production-ready code using a multi-agent system. The platform supports three main capabilities: Paper2Code (algorithm implementation), Text2Web (frontend development), and Text2Backend (backend development).

## Development Commands

### Installation & Setup
```bash
# Install from PyPI (recommended)
pip install deepcode-hku

# Development installation from source
git clone https://github.com/HKUDS/DeepCode.git
cd DeepCode/
pip install -r requirements.txt

# Using UV package manager (recommended for development)
uv venv --python=3.13
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Running the Application
```bash
# Web interface (recommended)
deepcode                              # If installed via pip
# OR for development:
streamlit run ui/streamlit_app.py    # Default port 8501
uv run streamlit run ui/streamlit_app.py  # Using UV

# CLI interface (advanced users)
python cli/main_cli.py
uv run python cli/main_cli.py        # Using UV
```

### Code Quality & Linting
```bash
# Pre-commit hooks (automatically configured)
pre-commit run --all-files

# Ruff formatting and linting
ruff format .
ruff check --fix --ignore=E402 .

# Manual dependency checks
pip check
```

### Testing
```bash
# No specific test framework configured - add tests as needed
# Check the codebase for testing patterns if implementing new tests
python -m pytest tests/  # If pytest is available
```

## Architecture Overview

### Core Components

**Multi-Agent System**: The platform uses a sophisticated multi-agent architecture coordinated by the `AgentOrchestrationEngine` (workflows/agent_orchestration_engine.py):

1. **Central Orchestrating Agent** - Strategic decision-making and workflow coordination
2. **Intent Understanding Agent** - Semantic analysis of user requirements 
3. **Document Parsing Agent** - Processing research papers and technical documents
4. **Code Planning Agent** - Architectural design and technology stack optimization
5. **Code Reference Mining Agent** - Repository discovery and analysis
6. **Code Indexing Agent** - Knowledge graph building and semantic relationships
7. **Code Generation Agent** - Code synthesis and implementation

**MCP (Model Context Protocol) Integration**: DeepCode leverages MCP servers for tool integration:
- `brave` / `bocha-mcp` - Web search engines
- `filesystem` - File operations
- `fetch` - Web content retrieval
- `github-downloader` - Repository management
- `code-implementation` - Code generation hub
- `code-reference-indexer` - Smart code search

### Directory Structure

```
DeepCode/
├── cli/                     # Command-line interface
│   ├── main_cli.py         # CLI entry point
│   ├── cli_interface.py    # CLI implementation
│   └── cli_app.py          # CLI application logic
├── ui/                     # Streamlit web interface
│   ├── streamlit_app.py    # Web app entry point
│   ├── components.py       # UI components
│   ├── handlers.py         # Event handlers
│   ├── layout.py           # Layout management
│   └── styles.py           # UI styling
├── workflows/              # Core workflow engines
│   ├── agent_orchestration_engine.py    # Main orchestrator
│   ├── code_implementation_workflow.py  # Code generation workflow
│   ├── codebase_index_workflow.py      # Code indexing workflow
│   └── agents/             # Specialized agent implementations
├── utils/                  # Utility modules
│   ├── file_processor.py   # File handling and processing
│   ├── dialogue_logger.py  # Conversation logging
│   ├── llm_utils.py       # LLM interaction utilities
│   └── cli_interface.py   # CLI utilities
├── prompts/               # Agent prompts and templates
├── config/               # Configuration files
├── tools/                # External tools and scripts
└── deepcode.py          # Main application launcher
```

### Configuration Files

**mcp_agent.config.yaml** - Primary configuration file:
- Search server settings (`brave` or `bocha-mcp`)
- Planning mode (`segmented` or `traditional`)
- Document segmentation settings
- MCP server configurations
- Logging settings

**mcp_agent.secrets.yaml** - API keys and secrets:
- OpenAI API configuration (api_key, base_url)
- Anthropic API key
- Search API keys (BRAVE_API_KEY, BOCHA_API_KEY)

## Key Development Patterns

### Agent Workflow Pattern
Agents follow a consistent async/await pattern with the MCP Agent framework:
```python
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm import RequestParams

# Agent implementation inherits from base Agent class
# Uses RequestParams for LLM configuration
# Implements async methods for agent coordination
```

### File Processing
The `FileProcessor` class (utils/file_processor.py) handles document processing:
- Supports PDF, DOCX, PPTX, TXT, HTML formats
- Intelligent document segmentation for large files
- LibreOffice integration for Office document conversion
- ReportLab for text-to-PDF conversion

### Memory Management
The system implements efficient memory mechanisms through specialized agents:
- `memory_agent_concise.py` - Basic memory management
- `memory_agent_concise_multi.py` - Multi-context memory
- `memory_agent_concise_index.py` - Indexed memory retrieval

### Workflow Modes
Two primary workflow modes available:
- **Traditional Mode**: Parallel agent execution (may hit token limits)
- **Segmented Mode**: Task breakdown to avoid token truncation (recommended)

## Environment Requirements

### Python Dependencies
- Python >= 3.9 (Python 3.13 recommended)
- Core: `streamlit`, `anthropic`, `aiofiles`, `aiohttp`, `mcp-agent`
- Document processing: `PyPDF2`, `reportlab`, `docling`
- System: `asyncio-mqtt`, `nest_asyncio`, `pathlib2`

### System Dependencies (Optional)
- **LibreOffice**: For Office document conversion
  - Windows: Download from https://www.libreoffice.org/
  - macOS: `brew install --cask libreoffice`
  - Ubuntu/Debian: `sudo apt-get install libreoffice`
- **Node.js**: Required for MCP servers
  - Install MCP servers: `npm i -g @modelcontextprotocol/server-brave-search`

### API Keys Setup
Configure API keys in `mcp_agent.secrets.yaml`:
- **OpenAI**: Required for code generation (`api_key`, `base_url`)
- **Anthropic**: Alternative LLM provider (`api_key`)
- **Brave Search**: Web search capability (`BRAVE_API_KEY`)
- **Bocha MCP**: Alternative search provider (`BOCHA_API_KEY`)

## Integration Points

### LLM Integration
The system supports multiple LLM providers through the MCP Agent framework:
- OpenAI GPT models (default)
- Anthropic Claude models
- Custom endpoints via `base_url` configuration

### Document Segmentation
Large documents automatically trigger intelligent segmentation when:
- Document size > 50,000 characters (configurable)
- Segmentation enabled in configuration
- Falls back to traditional processing for smaller documents

### Web Interface
Streamlit-based web interface with real-time progress tracking:
- Drag-and-drop file uploads
- Real-time agent status monitoring
- Interactive parameter configuration
- Download generated code and documentation

## Performance Considerations

### Memory Management
- Efficient context engineering for large codebases
- Hierarchical memory structures with intelligent compression
- Configurable token limits and truncation strategies

### Parallel Processing
- Multi-agent coordination with intelligent task distribution
- Async/await based high-performance execution
- Resource optimization and load balancing

### Caching
- Semantic vector embeddings for code discovery
- Knowledge graph caching for repository analysis
- Session-based memory persistence