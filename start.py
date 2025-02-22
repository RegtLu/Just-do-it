from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain.schema.runnable.passthrough import RunnableAssign
from langchain_core.runnables import RunnableBranch
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import gradio as gr
import os
from typing import *


os.environ["NVIDIA_API_KEY"] = ""


def better_embedding(documents: List[Document]) -> List[Document]:
    # 优化嵌入
    prompt = PromptTemplate(
        input_variables=["text"],
        template="请作为一名医生总结以下内容，提取症状，优化向量检索效果：\n{text}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    summarized_docs: List[Document] = []
    for doc in documents:
        summary = chain.run(text=doc.page_content)
        summarized_docs.append(
            Document(page_content=summary, metadata={"original_text": doc.page_content})
        )
    return summarized_docs


def better_query(query: str) -> str:
    # 优化查询
    prompt = PromptTemplate(
        input_variables=["query"],
        template="请作为一名医生改写以下查询，使症状更清晰，更适合向量检索：\n{query}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(query=query)


def get_documents(query: str) -> List[str]:
    query = better_query(query)
    results = retriever.get_relevant_documents(query)
    original_docs = [doc.metadata["original_text"] for doc in results]
    return original_docs


def query_rag(query: str) -> Tuple[str, List[str]]:
    docs = get_documents(query)
    prompt = PromptTemplate(
        input_variables=["context", "query"],
        template="以下是相关资料：\n{context}\n请作为一名医生根据这些信息回答问题：\n{query}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    final_answer = chain.run(context="\n".join(docs), query=query)
    return final_answer, docs


llm = ChatNVIDIA(model="ai-llama3-70b")
embeddings = NVIDIAEmbeddings(model="baai/bge-m3")
if os.path.exists("faiss_index"):
    vectorstore = FAISS.load_local("faiss_index", embeddings)
else:
    import build
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents_split = splitter.split_documents(build.build())
    documents_summarized = better_embedding(documents_split)
    vectorstore = FAISS.from_documents(documents_summarized, embeddings)
    vectorstore.save_local("faiss_index")
retriever = VectorStoreRetriever(vectorstore=vectorstore)


def response(history, message, source_list):
    query = '\n\n'.join(['用户：'+msg[0]+'\n回答：'+msg[1] for msg in history]) + '\n\n用户：' + message
    answer, sources = query_rag(query)
    history.append((message, answer))
    source_list = sources[:4]
    return history, *source_list

def clear(_):
    return [[]]*2+[""] * 4

with gr.Blocks() as demo:
    gr.Markdown("# Demo")
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot()
            user_input = gr.Textbox(placeholder="请输入你的消息...")
            send_button = gr.Button("发送")
            clear_button = gr.Button("清空聊天")
        with gr.Column():
            source1 = gr.Textbox(label="来源1", lines=2, interactive=False)
            source2 = gr.Textbox(label="来源2", lines=2, interactive=False)
            source3 = gr.Textbox(label="来源3", lines=2, interactive=False)
            source4 = gr.Textbox(label="来源4", lines=2, interactive=False)
    
    chat_history = gr.State([])
    file_list = gr.State([""] * 5)
    
    send_button.click(fn=response, 
                      inputs=[chat_history, user_input, file_list], 
                      outputs=[chatbot, source1, source2, source3, source4])
    clear_button.click(fn=clear, 
                       inputs=[file_list], 
                       outputs=[chatbot, chat_history, source1, source2, source3, source4])

demo.launch(debug=True, share=False, show_api=False, server_port=5000, server_name="0.0.0.0")