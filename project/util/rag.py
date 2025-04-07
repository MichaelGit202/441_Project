#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) Demo Script
Using ChromaDB for vector storage, chunking, and Ollama for both embeddings and LLM generation

To use RAG util:

use the following import:
from rag_test import retrieve_context_tool

Make sure the template json has the following tool:
{
      "type": "function",
      "function": {
        "name": "retrieve_context_tool",
        "description": "Used to retrieve context from files containing data that may be relevant to users' questions.",
        "parameters": {
          "type": "object",
          "properties": { 
            "user_prompt": {"type" : "string"}
          }
        }
      }
    }

"""


import os
import glob
import time
from typing import List, Dict, Any

# Vector database, embedding, and text processing
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter


import ollama
import numpy as np

# Utility imports
import pandas as pd
from util.llm_utils import run_console_chat, tool_tracker
from util.llm_utils import TemplateChat

collection = None


class OllamaEmbeddingFunction:
    """Custom embedding function that uses Ollama for embeddings"""
    
    def __init__(self, model_name="nomic-embed-text"):
        self.model_name = model_name
    
    ##Function to complete
    def __call__(self, input: List[str]) -> List[List[float]]:
        embeddings = ollama.embed(model = self.model_name, input = input)
        result = embeddings.get("embeddings",[])
        return result


def load_documents(data_dir: str) -> Dict[str, str]:
    """
    Load text documents from a directory
    """
    documents = {}
    for file_path in glob.glob(os.path.join(data_dir, "*.txt")):
        with open(file_path, 'r') as file:
            content = file.read()
            documents[os.path.basename(file_path)] = content
    
    print(f"Loaded {len(documents)} documents from {data_dir}")
    return documents


def chunk_documents(documents: Dict[str, str], chunk_size: int = 500, chunk_overlap: int = 50) -> List[Dict[str, Any]]:
    """
    Split documents into smaller chunks for embedding,
    using LangChain's RecursiveCharacterTextSplitter


    chunk_size will change the amount of characters in a chunk
    chunk_overlap sets the overlap of characters from one chunk to the next
    """
    chunked_documents = []
    
    # Create the chunker with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    for doc_name, content in documents.items():
        # Apply the chunker to the document text
        
        chunks = text_splitter.split_text(content)
        
        for i, chunk in enumerate(chunks):
            chunked_documents.append({
                "id": f"{doc_name}_chunk_{i}",
                "text": chunk,
                "metadata": {"source": doc_name, "chunk": i}
          })
    
    print(f"Created {len(chunked_documents)} chunks from {len(documents)} documents")
    return chunked_documents


def setup_chroma_db(chunks: List[Dict[str, Any]], collection_name: str = "dnd_knowledge", use_ollama_embeddings: bool = True, ollama_model: str = "nomic-embed-text") -> chromadb.Collection:
    """
    Set up ChromaDB with document chunks
    """
    # Initialize ChromaDB Ephemeral client
    client = chromadb.Client()
    # Initialize ChromaDB Persistent client - uncommenting next line will make a persistent database at the specified path
    #client = chromadb.PersistentClient(path="/path/to/save/to")
    
    # Create embedding function
    # Use custom Ollama embedding function
    embedding_function = OllamaEmbeddingFunction(model_name=ollama_model)
    print(f"Using Ollama for embeddings with model: {ollama_model}")
    
    # Create or get collection
    try:
        client.delete_collection(collection_name)
    except:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function
    )
    
    # Add documents to collection
    print(len(chunks))
    collection.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        metadatas=[chunk["metadata"] for chunk in chunks]
    )
    
    print(f"Added {len(chunks)} chunks to ChromaDB collection '{collection_name}'")
    return collection

def retrieve_context(collection: chromadb.Collection, query: str, n_results: int = 3) -> List[str]:
    """
    Retrieve relevant context from ChromaDB based on the query
    """

    result = collection.query(
            query_texts = [query], 
            n_results = n_results,
        )
    print("\n\nCOnTEXT: \n")
    print(result)
    print("\n\n")
    return [str(result['documents'])]


#shouldn't need
def generate_response(query: str, contexts: List[str], model: str = "mistral:latest") -> str:
    """
    Generate a response using Ollama LLM with the retrieved context
    """
    # Create prompt with context
    context_text = "\n\n".join(contexts)
    
    prompt = f"""You are a helpful tutor who is answering the questions of a student to aid in their studies.
    Use the following information to answer the question.
    
    Context:
    {context_text}
    
    Question: {query}
    
    Answer:"""
    
    response = ollama.generate(
        model=model,
        prompt=prompt,
    )
    
    return response["response"]

#Shouldn't need
def display_results(query: str, contexts: List[str], response: str) -> None:
    """
    Display the results in a formatted way
    """
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    print("\nCONTEXT USED:")
    print("-"*80)
    for i, context in enumerate(contexts, 1):
        print(f"Context {i}:")
        print(context[:200] + "..." if len(context) > 200 else context)
        print()
    
    print("\nGENERATED RESPONSE:")
    print("-"*80)
    print(response)
    print("="*80 + "\n")

#NEW: Tool Call
@tool_tracker
def retrieve_context_tool(user_prompt: str) -> List[str]:
    """
    Tool-callable function for LLM to retrieve context using RAG pipeline.
    Args:
        user_prompt (str): Original prompt from user.
    Returns:
        List[str]: Relevant context strings from vector store.
    """
    # Initialize embedding function
    embedding_fn = OllamaEmbeddingFunction()

    # Embed the prompt
    embedded_prompt = embedding_fn([user_prompt])[0]

    # Retrieve context using ChromaDB (embedding-based query)
    result = collection.query(
        query_embeddings=[embedded_prompt],
        n_results=5,
    )

    return str(result.get("documents", []))

@tool_tracker
def process_function_call(function_call):
    name = function_call.name
    args = function_call.arguments

    return globals()[name](**args)

def process_response(self, response):

    if response.message.tool_calls:
        self.messages.append({'role': 'tool',
                            'name': response.message.tool_calls[0].function.name, 
                            'arguments': response.message.tool_calls[0].function.arguments,
                            'content': process_function_call(response.message.tool_calls[0].function)
                            })
    response = self.completion()

    return response


def setup():
    global collection

    # Set embedding and LLM models
    embedding_model = "nomic-embed-text"  # Change to your preferred embedding model
    llm_model = "llama3.2:latest"  # Change to your preferred LLM model
    
    # 1. Load documents
    data_dir = "project/util/rag_documents"
    documents = load_documents(data_dir)
    
    # 2. Chunk documents using ChromaDB chunker
    chunks = chunk_documents(documents)
    
    # 3. Set up ChromaDB with Ollama embeddings
    collection = setup_chroma_db(
        chunks, 
        ollama_model=embedding_model
    )
    print("SETUP COMPLETE.")

def getCollection():
    return collection

def main():
    """
    Main function to run the RAG demo
    """
    
    setup()
    
    #Test tool call



    query = "What is the airspeed velocity of an unladen swallow?"
    #contexts = retrieve_context_tool(query)

    run_console_chat(template_file='project/util/templates/dm_chat.json',
                 process_response=process_response)

    #Old main function
    """
    # 4. Example queries
    queries = [
        "If the page size is increased by 32 bytes in both virtual and physical memories, how does such change affect an instruction execution in the CPU and writing into/reading from the hard disk?"
    ]
    
    # 5. Run RAG for each query
    for query in queries:
        # Retrieve context
        contexts = retrieve_context(collection, query, 10)
        
        # Generate response
        response = generate_response(query, contexts, model=llm_model)
        
        # Display results
        display_results(query, contexts, response)
    """
    



if __name__ == "__main__":
    main() 