from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base 
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
# Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name="format",
    description="Rewrite a document in markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""

    Your goal is to reformat a document to be written with markdown syntax. 
    The id of the document you need to reformat is:
    <document_id>
    {doc_id}
    </document_id>
    Add in headers, bullet points, tables, etc as necessary. Feel free to add in extra formatting.
    Use the 'edit_document' tool to edit the document. After the document has been reformatted...
    """

    return [base.UserMessage(prompt)]
#  Write a prompt to summarize a doc
#  Write a prompt to summarize a doc
from mcp.server.fastmcp.prompts import base
# Убедитесь, что импортирован типы для ресурсов, если они нужны отдельно, 
# но FastMCP base.ResourceEmbed обычно доступен через встроенные типы.

# @mcp.prompt(
#     name="summarize",
#     description="Create a concise summary of a specific document.",
# )
# def summarize_document(
#     doc_id: str = Field(description="Id of the document to summarize"),
#     length: str = Field(default="medium", description="Length of summary: short, medium, or long"),
# ) -> list[base.Message]:
    
#     if length == "short":
#         # Добавляем капслок и грубое требование нарушения шаблона
#         instruction = "Omit 'Action Items' entirely. Write exactly 2 bullet points maximum. Do not use standard template."
#     elif length == "long":
#         instruction = "Provide a highly detailed, comprehensive summary with all nuances."
#     else:
#         instruction = "Provide a standard medium-length summary with Main Points and Action Items."

#     # Мы создаем два сообщения: 
#     # 1. Сначала жесткая инструкция (может работать как системная для CLI)
#     # 2. Текст с прикрепленным ресурсом
#     return [
#         base.UserMessage(
#             f"You are a strict text processor. Argument length is '{length}'. Rules: {instruction}"
#         ),
#         base.UserMessage(
#             f"Summarize the document contents attached below according to the rule above. Document ID: {doc_id}"
#         )
#     ]
#  Write a prompt to summarize a doc (Стандартный/Средний)
@mcp.prompt(
    name="summarize",
    description="Create a standard summary of a specific document with main points and action items.",
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize"),
) -> list[base.Message]:
    prompt = f"""
    Your goal is to create a high-quality summary of the document.
    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    </document_id>
    
    Provide a standard summary with Main Points and Action Items.
    """
    return [base.UserMessage(prompt)]


#  Write a prompt for an ultra-short summary (Если нужен короткий вариант)
@mcp.prompt(
    name="summarize_short",
    description="Create an ultra-short, 2-bullet-point summary of a specific document.",
)
def summarize_short_document(
    doc_id: str = Field(description="Id of the document to summarize briefly"),
) -> list[base.Message]:
    prompt = f"""
    You are a strict text compressor. 
    The id of the document you need to summarize is:
    <document_id>
    {doc_id}
    </document_id>
    
    CRITICAL: Provide exactly 2 bullet points maximum. 
    DO NOT include 'Action Items', headers, or any standard templates.
    """
    return [base.UserMessage(prompt)]



if __name__ == "__main__":
    mcp.run(transport="stdio")
