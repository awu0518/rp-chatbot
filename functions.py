from langchain_core.documents import Document

def embed_text(filepath: str, filename: str) -> list[Document]:
    documents = []
    curr_str = ""
    file = open(filepath, "r")

    for line in file.readlines():
        if line == "=========================================================\n":
            doc = Document(
                page_content=curr_str,
                metadata={"file_name": filename}
            )

            documents.append(doc)
            curr_str = ""
        else:
            curr_str += line

    documents.append(Document(
                page_content=curr_str,
                metadata={"file_name": filename}
            ))
    return documents
