from mcp.server.fastmcp import FastMCP
from pydantic import Field
mcp = FastMCP("DocumentMCP", log_level="ERROR")
# uv run mcp dev mcp_server.py
#MCP Inspector = Postman - инструмент для MCP server in browser.
#И самое важное: Claude здесь пока вообще не нужен.
docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# 
# Write a tool to read a doc
#THIS IS MCP SDK (It imports the tools to build the schema)
# from mcp.server.fastmcp import FastMCP
# from pydantic import Field
@mcp.tool( #MCP SDK: Registers this function as an AI tool
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
#my business logic for the tool
def read_document(
     #MCP SDK: Builds the schema definition for Claude
    doc_id: str = Field(description="Id of the document to read"),
):
    if doc_id not in docs:
            raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]
#  Write a tool to edit a doc
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(
        description="The text to replace. Must match exactly, including whitespace"
    ),
    new_str: str = Field(
        description="The new text to insert in place of the old text"
    ),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
#for test MCP Inspector uv run mcp dev mcp_server.py / resources    
#  Write a resource to return all doc id's
#  # Return a list of all document ids
@mcp.resource(
     "docs://documents",
     mime_type="application/json",  #  
)

def list_docs() -> list[str]:
    return list(docs.keys())
#  Write a resource to return the contents of a particular doc
# it needs for autocompletion of the doc_id in the prompt.
# Пользователь: @report Клиент gолучает docs://documents 
# report.pdf report_final.pdf
# Пользователь выбирает: @report.pdf Клиент получает:
#docs://documents/report.pdf  содержимое.  

@mcp.resource(
     "docs://documents/{doc_id}",
     mime_type="text/plain",
   
)
# Return the contents of a template (particular doc_id) document
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
