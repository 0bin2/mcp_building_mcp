# MCP Documentation Search Server

A comprehensive Model Context Protocol (MCP) server that provides powerful search and browsing capabilities for MCP documentation and Python SDK content. This server enables efficient exploration of MCP concepts, implementation details, and code examples through intelligent parsing and search functionality.

## 🚀 Features

### 📚 **Resource Browsing**
- **Section Listing** - Browse all available documentation sections with metadata
- **Full Section Content** - Access complete content of any documentation section
- **Core Concepts Overview** - Quick access to fundamental MCP concepts

### 🔍 **Advanced Search Tools**
- **Section Name Search** - Find sections by title and header names
- **Content Text Search** - Full-text search within documentation content
- **Implementation Requirements** - Locate imports, dependencies, and setup instructions
- **Contextual Results** - Search results include surrounding context for better understanding

### 📊 **Rich Metadata**
- Document type classification (MCP Documentation vs Python SDK)
- Header level hierarchy (H1, H2, H3, etc.)
- Word count statistics
- Match frequency analysis

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- MCP Python SDK

### Dependencies
```bash
pip install "mcp[cli]"
```

### Quick Setup
1. Save the server file as `mcp_docs_server.py`
2. Make it executable: `chmod +x mcp_docs_server.py`

## 🏃 Running the Server

### Development Mode
Test and debug your server with the MCP Inspector:
```bash
mcp dev mcp_docs_server.py
```

### Claude Desktop Integration
Install the server in Claude Desktop for seamless integration:
```bash
mcp install mcp_docs_server.py --name "MCP Documentation Search"
```

### Direct Execution
Run the server directly:
```bash
python mcp_docs_server.py
```

## 🔧 API Reference

### Resources

#### `mcp://sections/list`
Get a comprehensive list of all available documentation sections.

**Returns:** Hierarchical list of sections with metadata including:
- Section names and titles
- Document type (MCP Documentation/Python SDK)
- Header level hierarchy
- Word count for each section

#### `mcp://section/{section_name}`
Retrieve the complete content of a specific documentation section.

**Parameters:**
- `section_name` (string): Exact name of the section to retrieve

**Returns:** Full section content with metadata

#### `mcp://concepts/core`
Access an overview of core MCP concepts including servers, resources, tools, and prompts.

**Returns:** Curated overview of fundamental MCP concepts with examples

### Tools

#### `search_sections_by_name(keyword, case_sensitive=False, max_results=10)`
Search for documentation sections by section names containing the specified keyword.

**Parameters:**
- `keyword` (string): The keyword to search for in section names
- `case_sensitive` (boolean): Whether to perform case-sensitive search (default: False)
- `max_results` (integer): Maximum number of results to return (default: 10)

**Returns:** List of matching sections with previews and metadata

**Example:**
```python
# Find all sections related to FastMCP
search_sections_by_name("FastMCP")

# Case-sensitive search for tools
search_sections_by_name("Tools", case_sensitive=True, max_results=5)
```

#### `search_content_by_text(keyword, case_sensitive=False, max_results=10)`
Search for sections containing the keyword in their content text.

**Parameters:**
- `keyword` (string): The keyword to search for in content text
- `case_sensitive` (boolean): Whether to perform case-sensitive search (default: False)
- `max_results` (integer): Maximum number of results to return (default: 10)

**Returns:** List of matching sections with contextual snippets around matches

**Example:**
```python
# Find content about tool decorators
search_content_by_text("@mcp.tool")

# Search for import statements
search_content_by_text("import", max_results=15)
```

#### `get_section_details(section_name)`
Get the complete content of a specific documentation section.

**Parameters:**
- `section_name` (string): The exact name of the section to retrieve

**Returns:** Full section content with comprehensive metadata

**Example:**
```python
# Get details about core concepts
get_section_details("Python SDK: Core Concepts")
```

#### `find_implementation_requirements(keyword)`
Find implementation requirements, imports, and dependencies for a specific MCP feature or concept.

**Parameters:**
- `keyword` (string): The feature or concept to find requirements for

**Returns:** Requirements, imports, and implementation details with code examples

**Example:**
```python
# Find FastMCP implementation requirements
find_implementation_requirements("FastMCP")

# Get server setup requirements
find_implementation_requirements("server")
```

## 📖 Usage Examples

### Basic Search Operations

```python
# Browse available sections
sections = get_resource("mcp://sections/list")

# Search for authentication-related content
auth_sections = search_sections_by_name("auth")

# Find all mentions of decorators in content
decorator_content = search_content_by_text("@mcp")

# Get complete implementation details
server_details = get_section_details("Python SDK: Server")
```

### Advanced Search Patterns

```python
# Find specific implementation patterns
fastmcp_requirements = find_implementation_requirements("FastMCP")

# Search for error handling examples
error_examples = search_content_by_text("try:", max_results=20)

# Locate transport configuration
transport_sections = search_sections_by_name("transport", case_sensitive=False)
```

### Working with Search Results

Each search result includes rich metadata:
- **Section name and title**
- **Document source** (MCP Documentation or Python SDK)
- **Header level** for navigation hierarchy
- **Word count** for content estimation
- **Match context** or preview snippets
- **Match frequency** for relevance ranking

## 🏗️ Architecture

### Document Parser
The `DocumentParser` class handles:
- **Markdown parsing** with header-level organization
- **Section extraction** based on heading hierarchy
- **Metadata generation** including word counts and document classification
- **Search indexing** for efficient content retrieval

### Search Algorithms
- **Name-based search**: Pattern matching in section titles and headers
- **Content-based search**: Full-text search with contextual snippet extraction
- **Requirement extraction**: Intelligent parsing of code blocks and dependencies
- **Relevance ranking**: Results sorted by match frequency and section importance

### Content Organization
- **Hierarchical structure**: Maintains document header hierarchy (H1-H6)
- **Cross-referencing**: Links between related concepts and implementations
- **Metadata enrichment**: Automatic classification and statistics generation

## 🔧 Configuration

### Customizing Search Behavior
Modify search parameters in the `DocumentParser` class:
- Adjust context window size for content search
- Configure result ranking algorithms
- Customize section parsing patterns

### Adding Content Sources
To add additional documentation sources:
1. Add content to the parser initialization
2. Update document type classification
3. Ensure proper markdown parsing

## 🐛 Troubleshooting

### Common Issues

**Server not connecting:**
- Ensure MCP Python SDK is properly installed
- Check that the server file has proper permissions
- Verify no port conflicts exist

**Search returns no results:**
- Check keyword spelling and capitalization
- Try broader search terms
- Use `list_all_sections()` to see available content

**Performance issues:**
- Reduce `max_results` parameter for large searches
- Use more specific keywords to narrow results
- Consider case-sensitive search for exact matches

### Debug Mode
Run with verbose logging:
```bash
mcp dev mcp_docs_server.py --verbose
```

## 🤝 Contributing

### Development Setup
1. Clone or download the server file
2. Install development dependencies
3. Run tests with the MCP Inspector

### Adding Features
- **New search algorithms**: Extend the `DocumentParser` class
- **Additional metadata**: Enhance section parsing logic
- **Custom resources**: Add new resource endpoints
- **Tool improvements**: Extend existing tool functionality

## 📄 License

This project follows the same license as the MCP Python SDK (MIT License).

## 🔗 Related Links

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Claude Desktop](https://claude.ai/download)

## 🆘 Support

For issues related to:
- **MCP Documentation Search Server**: Create an issue in your repository
- **MCP Protocol**: Visit [MCP GitHub Discussions](https://github.com/modelcontextprotocol/python-sdk/discussions)
- **Python SDK**: Check the [official SDK documentation](https://modelcontextprotocol.io)

---

**Made with ❤️ for the MCP Community**