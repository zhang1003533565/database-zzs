from typing import TypedDict
from langgraph.graph import StateGraph
from .config import get_llm

llm = get_llm()

# ✅ 修复非法字符（如 emoji、系统符号）导致的 encode 错误
def safe_text(text: str) -> str:
    return text.encode("utf-8", "ignore").decode("utf-8")

# 状态结构
class QAState(TypedDict):
    input: str
    output: str
    next: str
    history: list[str]

# 判断是否需要“搜索”
def classify_question(state: QAState) -> QAState:
    if "今天" in state["input"] or "天气" in state["input"]:
        return {**state, "next": "search"}
    else:
        return {**state, "next": "direct"}

# 普通问答（记忆 + 编码安全）
def direct_answer(state: QAState) -> QAState:
    conversation = "\n".join(safe_text(x) for x in state["history"] + [f"用户：{state['input']}"])
    response = llm.invoke(f"以下是与用户的对话，请回答最后一条提问：\n{conversation}")
    return {
        **state,
        "output": response.content,
        "history": state["history"] + [f"用户：{state['input']}", f"助手：{response.content}"]
    }

# 模拟搜索后回答
def search_and_answer(state: QAState) -> QAState:
    info = "模拟搜索结果：今天天气晴，气温22°C。"
    conversation = "\n".join(safe_text(x) for x in state["history"] + [f"用户：{state['input']}"])
    response = llm.invoke(f"结合'{info}'信息，回答以下对话内容：\n{conversation}")
    return {
        **state,
        "output": response.content,
        "history": state["history"] + [f"用户：{state['input']}", f"助手：{response.content}"]
    }

# 构建 LangGraph 流程图
def build_graph():
    graph = StateGraph(QAState)
    graph.add_node("classify", classify_question)
    graph.add_node("direct", direct_answer)
    graph.add_node("search", search_and_answer)
    graph.set_entry_point("classify")

    graph.add_conditional_edges("classify", lambda state: state["next"], {
        "direct": "direct",
        "search": "search"
    })

    graph.set_finish_point("direct")
    graph.set_finish_point("search")

    return graph.compile()
