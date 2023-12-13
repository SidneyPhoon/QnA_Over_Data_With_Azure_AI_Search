from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(search_result: object) -> str:
    def format_doc(doc: dict):
        return f"Content: {doc['Content']}\nSource: {doc['Source']}"

    retrieved_docs = []
    for doc in search_result:
        #print(doc["chunk"])
        content = doc["chunk"]
        #print(doc["title"])
        source = doc["title"]

        retrieved_docs.append({
            "Content": content,
            "Source": source
        })
    
    doc_string = "\n\n".join([format_doc(doc) for doc in retrieved_docs])
    return doc_string