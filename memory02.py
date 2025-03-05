from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

# チャットモデルの初期化
chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True)

# メモリの初期化
memory = ConversationBufferMemory()

# 会話チェーンの初期化（同じメモリインスタンスを使用）
conversation = ConversationChain(
    llm=chat,
    memory=memory,
    verbose=True
)

while True:
    try:
        # ユーザー入力の受け取り
        user_message = input("You: ")
        
        # 終了条件
        if user_message.lower() in ['quit', 'exit', 'bye']:
            print("会話を終了します")
            break
            
        # AIの応答を取得
        ai_message = conversation.predict(input=user_message)
        print(f"AI: {ai_message}")
        
    except KeyboardInterrupt:
        print("\n会話を終了します")
        break
    except Exception as e:
        print(f"エラーが発生しました: {e}")


