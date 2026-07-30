from langchain_groq import ChatGroq
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import HumanMessage, AIMessage


def prompts_and_chains(llm, retriever):
    # Prompt used to answer the user's question using the retrieved context
    qa_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful AI assistant. "
            "Answer the user's question only from the provided context and previous chat history. "
            "If the answer is not available in the context, say that you don't know."
        ),
        MessagesPlaceholder("chat_history"),
        (
            "human",
            "{input}\n\nContext:\n{context}"
        )
    ])

    # Prompt used to convert follow-up questions into standalone questions
    context_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Given the previous conversation, rewrite the user's latest question "
            "as a standalone question if needed. Do not answer the question."
        ),
        MessagesPlaceholder("chat_history"),
        (
            "human",
            "{input}"
        )
    ])

    # Creates a retriever that understands follow-up questions
    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        context_prompt
    )

    # Combines retrieved documents with the QA prompt
    question_answer_chain = create_stuff_documents_chain(
        llm,
        qa_prompt
    )

    # Complete RAG pipeline
    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain
    )

    return rag_chain


def generate_response(rag_chain, query, chat_history):
    # Invoke the RAG chain
    response = rag_chain.invoke({
        "input": query,
        "chat_history": chat_history
    })

    # Store the latest conversation for future follow-up questions
    chat_history.extend([
        HumanMessage(content=query),
        AIMessage(content=response["answer"])
    ])

    return response