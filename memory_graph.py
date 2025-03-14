# langgraphを使用して、8回以上の会話を要約する機能をテストしてます

from typing import Literal
from langchain_core.messages import SystemMessage, RemoveMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# ChatGPTモデルの初期化
model = ChatOpenAI(model_name="gpt-4", temperature=0)

memory = MemorySaver()  # 会話のデータを保存するためのメモリを初期化

# `messages`キー（MessagesStateクラスが持つ）に加えて、`summary`属性を追加します
class State(MessagesState):
    summary: str  # 会話の要約を保持するための属性

# モデルを呼び出すための処理を定義します
def call_model(state: State):
    # 要約が存在する場合、それをシステムメッセージとして追加します
    summary = state.get("summary", "")
    if summary:
        system_message = f"前回の会話の要約: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]  # 要約がない場合はそのまま使用します
    response = model.invoke(messages)  # モデルを呼び出し、応答を取得
    # メッセージをリスト形式で返す（既存のリストに追加されるため）
    return {"messages": [response]}

# 会話を続けるか要約を行うかを判断するための処理
def should_continue(state: State) -> Literal["summarize_conversation", END]:
    """次に実行するノードを返す"""
    messages = state["messages"]
    # メッセージが6個以上の場合は会話を要約
    if len(messages) > 7:
        return "summarize_conversation"
    # そうでない場合は会話を終了
    return END

# 会話を要約する処理を定義
def summarize_conversation(state: State):
    # 会話を最初に要約
    summary = state.get("summary", "")
    if summary:
        # 既存の要約がある場合はそれを拡張するシステムプロンプトを使用
        summary_message = (
            f"これまでの会話の要約: {summary}\n\n"
            "上記の新しいメッセージを考慮して要約を拡張してください:"
        )
    else:
        summary_message = "上記の会話の要約を作成してください:"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    # 表示したくないメッセージを削除（最新の2件以外のメッセージを削除）
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    print(response.content)
    return {"summary": response.content, "messages": delete_messages}

# 新しいワークフローグラフを定義
workflow = StateGraph(State)

# 会話ノードと要約ノードを追加
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

# 会話を開始点として設定
workflow.add_edge(START, "conversation")

# 条件付きの遷移を追加
workflow.add_conditional_edges(
    # スタートノードとして`conversation`を使用。
    # これは、`conversation`ノードが呼ばれた後に実行される遷移
    "conversation",
    # 次に実行するノードを決定する関数を指定
    should_continue,
)

# `summarize_conversation`からENDへの通常の遷移を追加。
# `summarize_conversation`が実行された後、会話が終了
workflow.add_edge("summarize_conversation", END)

# 最後にワークフローをコンパイル
app = workflow.compile(checkpointer=memory)

messages = [
    SystemMessage(content="あなたは親切な日本語教師です"),    
    HumanMessage(content="はじめまして、私の名前はマイクです"),
    AIMessage(content="マイクさん、はじめまして！日本語を勉強されているんですね"),
    HumanMessage(content="そうです。日本に旅行する予定です"),
    AIMessage(content="素晴らしいですね！いつ日本へ行く予定ですか？"),
    HumanMessage(content="来月です。おすすめのレストランはありますか？"),
    AIMessage(content="東京であれば、築地市場の寿司や浅草の天ぷら屋さんがおすすめです"),
    HumanMessage(content="ありがとう。電車の乗り方も教えてください"),
    AIMessage(content="日本の電車は非常に正確です。ICカード（Suicaなど）を購入すると便利ですよ"),
    HumanMessage(content="日本語で「お腹がすきました」はどう言いますか？"),
    AIMessage(content="そのまま「お腹がすきました」または「お腹が空きました」と言えますよ。カジュアルに「お腹すいた」とも言えます"),
]


config = {"configurable": {"thread_id": "abc789"}}
query = "私の名前を憶えてますか？"
language = "Japanese"
# ここでさきほど定義した長いmessagesに、名前を質問するプロンプトを追加して投げている。
input_messages = messages + [HumanMessage(query)]
print(input_messages)
print([HumanMessage(query)])
output = app.invoke(
    {"messages": input_messages, "language": language},
    config,
)
output["messages"][-1].pretty_print()