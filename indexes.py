from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# PDFファイルの読み込み
loader = DirectoryLoader("./data", glob="**/*.pdf")

try:
    # ドキュメントの読み込み
    documents = loader.load()
    print(f"読み込まれたドキュメント数: {len(documents)}")
    
    # embeddingsモデルを明示的に指定
    embeddings = OpenAIEmbeddings()
    
    # 永続的なベクトルストアを指定
    index = VectorstoreIndexCreator(
        vectorstore_cls=FAISS,  # 永続的なベクトルストアを使用
        embedding=embeddings
    ).from_loaders([loader])
    
except Exception as e:
    print(f"エラーが発生しました: {e}")
