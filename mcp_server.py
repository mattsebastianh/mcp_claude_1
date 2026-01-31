from mistune import markdown
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc_content",
    description="Reads the content of a document and returns it as string."
)
def read_doc(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc_content",
    description="Edits the content of a document replacing existing strings by new ones."
)
def edit_doc(
    doc_id: str = Field(description="Id of the document to edit"),
    old_strings: list[str] = Field(description="List of strings to be replaced in the document content"),
    new_strings: list[str] = Field(description="List of strings to replace the old strings in the document content"),
):
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    if len(old_strings) != len(new_strings):
        raise ValueError("The number of old_strings must match the number of new_strings.")
    
    for old_string, new_string in zip(old_strings, new_strings):
        docs[doc_id] = docs[doc_id].replace(old_string, new_string)
    
    return f"Document '{doc_id}' updated successfully."

# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json",
)
def list_docs() -> list[str]:
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain",
)
def fetch_doc_content(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Document with id '{doc_id}' not found.")
    return docs[doc_id]
    

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in markdown format."
)
def format_doc(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    prompt = f"""
    You are a document conversion specialist tasked with rewriting documents in markdown format. 
    Your goal is to reformat the given document and enhance its readability by adding 
    appropriate markdown syntax, while preserving the original content and meaning.

    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>

    Instructions:
    - Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
    - Use the 'edit_document' tool to edit the document. 
    - Use appropiate headers levels (#, ##, ###) to organize the document structure.
    - Properly format lists (ordered and unordered) and tables using markdown syntax.
    - Use emphasis syntax such as *italic* and **bold** where appropriate to enhance readability.
    - Add links using [link text](URL) format if there are any references to external resources.
    - Ensure that code snippets, if any, are properly formatted using triple backticks (```).
    - Maintain the original meaning and context of the document while improving its presentation.
    - After the document has been reformatted, present the reformated document in Markdown syntax. 
    - Use the ``` mark to denote the beginning and the end of the markdown content.

    Before providing the final Markdown output, in <document analysis> tags:
    - Identify the main sections and susbsections of the document
    - Count the number of the sections and subsections to ensure proper nesting of headers
    This will ensure that the document is well-structured, and conversion willl be correctly organized.

    Example output structure:
    <document analysis>
    [your analysis of the document structure and conversion plan]
    </document analysis>
    ```markdown
    # Document Title
    ## Section 1
    [Content of section 1...]
    - List item 1
    - List item 2
    ## Section 2
    [Content of section 2...]
    | Table Header 1 | Table Header 2 |
    |----------------|----------------|
    | Data 1         | Data 2         |
    ```

    Please proceed with your analysis and the markdown conversion of the document.
    """

    return [base.UserMessage(prompt)]

# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
