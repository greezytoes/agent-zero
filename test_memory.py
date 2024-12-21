from python.helpers.dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os
from langchain_community.vectorstores import FAISS

def test_memory():
    print("Loading environment variables...")
    load_dotenv()
    
    print("\nInitializing OpenAI embeddings model...")
    try:
        embedding_model = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_type="open_ai",
            openai_api_base="https://api.openai.com/v1"
        )
        
        print("\nTesting direct embedding...")
        test_text = "Hello, this is a test of the embeddings model."
        embedding = embedding_model.embed_query(test_text)
        print(f"Direct embedding successful! Vector length: {len(embedding)}")
        
        print("\nTesting FAISS vectorstore initialization...")
        texts = ["This is a test document"]
        
        # Create the vectorstore directly from texts
        vectorstore = FAISS.from_texts(
            texts=texts,
            embedding=embedding_model
        )
        
        print("\nTesting search...")
        results = vectorstore.similarity_search("test", k=1)
        print(f"Search results: {results[0].page_content}")
        
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        raise e

if __name__ == "__main__":
    test_memory()
