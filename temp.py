#!/usr/bin/env python3
"""
MCP Documentation Search Server

This server provides browsing and searching capabilities for the Model Context Protocol (MCP)
documentation and Python SDK. It exposes key concepts as resources and provides tools for
content search by section names and text content.

Dependencies:
- mcp[cli]
- re (built-in)
- typing (built-in)
"""

import re
from typing import List, Dict, Tuple, Optional
from mcp.server.fastmcp import FastMCP

# MCP Documentation content
MCP_DOCS_CONTENT = """<your_first_document_content_here>"""

# Python SDK README content
PYTHON_SDK_CONTENT = """<your_second_document_content_here>"""

# Initialize FastMCP server
mcp = FastMCP("MCP Documentation Search Server")


class DocumentParser:
    """Parser for MCP documentation and SDK content"""

    def __init__(self):
        self.mcp_sections = self._parse_sections(MCP_DOCS_CONTENT, "MCP Documentation")
        self.sdk_sections = self._parse_sections(PYTHON_SDK_CONTENT, "Python SDK")
        self.all_sections = {**self.mcp_sections, **self.sdk_sections}

    def _parse_sections(self, content: str, doc_type: str) -> Dict[str, Dict]:
        """Parse markdown content into sections based on headers"""
        sections = {}

        # Split by headers (# ## ### etc.)
        header_pattern = r"^(#{1,6})\s+(.+)$"
        lines = content.split("\n")

        current_section = None
        current_content = []
        current_level = 0

        for line in lines:
            header_match = re.match(header_pattern, line, re.MULTILINE)

            if header_match:
                # Save previous section if exists
                if current_section:
                    sections[current_section] = {
                        "title": current_section,
                        "content": "\n".join(current_content).strip(),
                        "level": current_level,
                        "doc_type": doc_type,
                        "word_count": len("\n".join(current_content).split()),
                    }

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = f"{doc_type}: {title}"
                current_content = [line]
                current_level = level
            else:
                if current_section:
                    current_content.append(line)

        # Don't forget the last section
        if current_section:
            sections[current_section] = {
                "title": current_section,
                "content": "\n".join(current_content).strip(),
                "level": current_level,
                "doc_type": doc_type,
                "word_count": len("\n".join(current_content).split()),
            }

        return sections

    def search_by_section_name(
        self, keyword: str, case_sensitive: bool = False
    ) -> List[Dict]:
        """Search for sections containing keyword in section names"""
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()

        for section_name, section_data in self.all_sections.items():
            search_name = section_name if case_sensitive else section_name.lower()

            if search_keyword in search_name:
                results.append(
                    {
                        "section_name": section_name,
                        "doc_type": section_data["doc_type"],
                        "level": section_data["level"],
                        "word_count": section_data["word_count"],
                        "preview": (
                            section_data["content"][:200] + "..."
                            if len(section_data["content"]) > 200
                            else section_data["content"]
                        ),
                    }
                )

        return sorted(results, key=lambda x: x["level"])

    def search_by_content_text(
        self, keyword: str, case_sensitive: bool = False
    ) -> List[Dict]:
        """Search for sections containing keyword in content text"""
        results = []
        search_keyword = keyword if case_sensitive else keyword.lower()

        for section_name, section_data in self.all_sections.items():
            search_content = (
                section_data["content"]
                if case_sensitive
                else section_data["content"].lower()
            )

            if search_keyword in search_content:
                # Find context around the keyword
                content_lines = section_data["content"].split("\n")
                matching_lines = []

                for i, line in enumerate(content_lines):
                    search_line = line if case_sensitive else line.lower()
                    if search_keyword in search_line:
                        # Get context (line before, matching line, line after)
                        context_start = max(0, i - 1)
                        context_end = min(len(content_lines), i + 2)
                        context = content_lines[context_start:context_end]
                        matching_lines.extend(context)

                results.append(
                    {
                        "section_name": section_name,
                        "doc_type": section_data["doc_type"],
                        "level": section_data["level"],
                        "word_count": section_data["word_count"],
                        "matching_context": "\n".join(
                            matching_lines[:10]
                        ),  # Limit context
                        "match_count": search_content.count(search_keyword),
                    }
                )

        return sorted(results, key=lambda x: x["match_count"], reverse=True)

    def get_section_content(self, section_name: str) -> Optional[Dict]:
        """Get full content of a specific section"""
        return self.all_sections.get(section_name)

    def get_section_list(self) -> List[Dict]:
        """Get list of all available sections"""
        return [
            {
                "section_name": name,
                "doc_type": data["doc_type"],
                "level": data["level"],
                "word_count": data["word_count"],
            }
            for name, data in self.all_sections.items()
        ]


# Initialize parser
doc_parser = DocumentParser()


# Resources - Expose key concepts and sections
@mcp.resource("mcp://sections/list")
def list_all_sections() -> str:
    """Get a list of all available documentation sections from MCP docs and Python SDK"""
    sections = doc_parser.get_section_list()

    result = "# Available Documentation Sections\n\n"

    # Group by document type
    mcp_sections = [s for s in sections if s["doc_type"] == "MCP Documentation"]
    sdk_sections = [s for s in sections if s["doc_type"] == "Python SDK"]

    result += "## MCP Documentation Sections:\n"
    for section in sorted(mcp_sections, key=lambda x: x["level"]):
        indent = "  " * (section["level"] - 1)
        result += (
            f"{indent}- {section['section_name']} ({section['word_count']} words)\n"
        )

    result += "\n## Python SDK Sections:\n"
    for section in sorted(sdk_sections, key=lambda x: x["level"]):
        indent = "  " * (section["level"] - 1)
        result += (
            f"{indent}- {section['section_name']} ({section['word_count']} words)\n"
        )

    return result


@mcp.resource("mcp://section/{section_name}")
def get_section_content(section_name: str) -> str:
    """Get the full content of a specific documentation section

    Args:
        section_name: The name of the section to retrieve (e.g., "MCP Documentation: Overview")
    """
    section_data = doc_parser.get_section_content(section_name)

    if not section_data:
        return f"Section '{section_name}' not found. Use mcp://sections/list to see available sections."

    result = f"# {section_data['title']}\n\n"
    result += f"**Document Type:** {section_data['doc_type']}\n"
    result += f"**Header Level:** {section_data['level']}\n"
    result += f"**Word Count:** {section_data['word_count']}\n\n"
    result += "## Content:\n\n"
    result += section_data["content"]

    return result


@mcp.resource("mcp://concepts/core")
def get_core_concepts() -> str:
    """Get an overview of core MCP concepts including servers, resources, tools, and prompts"""
    concepts = []

    # Look for core concept sections
    core_keywords = [
        "core concepts",
        "overview",
        "server",
        "resources",
        "tools",
        "prompts",
        "what is mcp",
    ]

    for keyword in core_keywords:
        results = doc_parser.search_by_section_name(keyword, case_sensitive=False)
        concepts.extend(results[:2])  # Limit results per keyword

    result = "# Core MCP Concepts\n\n"
    result += "This resource provides an overview of the fundamental concepts in the Model Context Protocol.\n\n"

    seen_sections = set()
    for concept in concepts:
        if concept["section_name"] not in seen_sections:
            seen_sections.add(concept["section_name"])
            result += f"## {concept['section_name']}\n"
            result += f"**Source:** {concept['doc_type']}\n\n"
            result += f"{concept['preview']}\n\n"

    return result


# Tools - Search functionality
@mcp.tool()
def search_sections_by_name(
    keyword: str, case_sensitive: bool = False, max_results: int = 10
) -> str:
    """Search documentation sections by section name containing the specified keyword

    Args:
        keyword: The keyword to search for in section names
        case_sensitive: Whether to perform case-sensitive search (default: False)
        max_results: Maximum number of results to return (default: 10)

    Returns:
        Formatted search results showing matching sections with previews
    """
    results = doc_parser.search_by_section_name(keyword, case_sensitive)

    if not results:
        return f"No sections found with '{keyword}' in the section name."

    limited_results = results[:max_results]

    response = f"# Search Results for '{keyword}' in Section Names\n\n"
    response += f"Found {len(results)} section(s) (showing {len(limited_results)}):\n\n"

    for i, result in enumerate(limited_results, 1):
        response += f"## {i}. {result['section_name']}\n"
        response += f"**Source:** {result['doc_type']}\n"
        response += f"**Level:** H{result['level']}\n"
        response += f"**Word Count:** {result['word_count']}\n"
        response += f"**Preview:** {result['preview']}\n\n"

    if len(results) > max_results:
        response += f"... and {len(results) - max_results} more results. Increase max_results to see more.\n"

    return response


@mcp.tool()
def search_content_by_text(
    keyword: str, case_sensitive: bool = False, max_results: int = 10
) -> str:
    """Search documentation content by text containing the specified keyword

    Args:
        keyword: The keyword to search for in content text
        case_sensitive: Whether to perform case-sensitive search (default: False)
        max_results: Maximum number of results to return (default: 10)

    Returns:
        Formatted search results showing matching content with context around matches
    """
    results = doc_parser.search_by_content_text(keyword, case_sensitive)

    if not results:
        return f"No content found containing '{keyword}' in the text."

    limited_results = results[:max_results]

    response = f"# Search Results for '{keyword}' in Content Text\n\n"
    response += f"Found {len(results)} section(s) with matches (showing {len(limited_results)}):\n\n"

    for i, result in enumerate(limited_results, 1):
        response += f"## {i}. {result['section_name']}\n"
        response += f"**Source:** {result['doc_type']}\n"
        response += f"**Level:** H{result['level']}\n"
        response += f"**Matches:** {result['match_count']}\n"
        response += f"**Word Count:** {result['word_count']}\n"
        response += "**Context:**\n```\n"
        response += result["matching_context"]
        response += "\n```\n\n"

    if len(results) > max_results:
        response += f"... and {len(results) - max_results} more results. Increase max_results to see more.\n"

    return response


@mcp.tool()
def get_section_details(section_name: str) -> str:
    """Get the complete content of a specific documentation section

    Args:
        section_name: The exact name of the section to retrieve

    Returns:
        The full content of the specified section with metadata
    """
    section_data = doc_parser.get_section_content(section_name)

    if not section_data:
        available_sections = [name for name in doc_parser.all_sections.keys()][:10]
        response = f"Section '{section_name}' not found.\n\n"
        response += "Available sections (first 10):\n"
        for section in available_sections:
            response += f"- {section}\n"
        response += "\nUse search_sections_by_name() to find specific sections."
        return response

    response = f"# {section_data['title']}\n\n"
    response += "## Metadata\n"
    response += f"- **Document Type:** {section_data['doc_type']}\n"
    response += f"- **Header Level:** H{section_data['level']}\n"
    response += f"- **Word Count:** {section_data['word_count']}\n\n"
    response += "## Full Content\n\n"
    response += section_data["content"]

    return response


@mcp.tool()
def find_implementation_requirements(keyword: str) -> str:
    """Find implementation requirements, imports, and dependencies for a specific MCP feature or concept

    Args:
        keyword: The feature or concept to find requirements for (e.g., "FastMCP", "server", "tools")

    Returns:
        Requirements, imports, and implementation details for the specified feature
    """
    # Search for content related to requirements, imports, dependencies
    search_terms = [
        "import",
        "dependencies",
        "install",
        "requirements",
        "from mcp",
        "pip install",
    ]

    all_matches = []

    # First search by the main keyword
    main_results = doc_parser.search_by_content_text(keyword, case_sensitive=False)

    # Then look for requirement-related content in those results
    for result in main_results[:5]:  # Check top 5 matches
        section_content = result["matching_context"]

        for term in search_terms:
            if term.lower() in section_content.lower():
                all_matches.append(
                    {
                        "section": result["section_name"],
                        "doc_type": result["doc_type"],
                        "content": section_content,
                        "requirement_type": term,
                    }
                )
                break

    if not all_matches:
        return f"No implementation requirements found for '{keyword}'. Try searching for the concept first."

    response = f"# Implementation Requirements for '{keyword}'\n\n"

    seen_sections = set()
    for match in all_matches:
        if match["section"] not in seen_sections:
            seen_sections.add(match["section"])
            response += f"## {match['section']}\n"
            response += f"**Source:** {match['doc_type']}\n"
            response += f"**Requirement Type:** {match['requirement_type']}\n\n"
            response += "```python\n"

            # Extract code-like lines
            lines = match["content"].split("\n")
            code_lines = []
            for line in lines:
                if any(
                    code_indicator in line.lower()
                    for code_indicator in [
                        "import",
                        "from ",
                        "pip install",
                        "uv add",
                        "dependencies",
                    ]
                ):
                    code_lines.append(line.strip())

            if code_lines:
                response += "\n".join(code_lines)
            else:
                response += match["content"]

            response += "\n```\n\n"

    return response


if __name__ == "__main__":
    # You need to replace the placeholder content with actual data
    print("MCP Documentation Search Server")
    print(
        "Make sure to replace MCP_DOCS_CONTENT and PYTHON_SDK_CONTENT with actual document content"
    )
    print("Then run with: mcp dev this_file.py")
    mcp.run()
