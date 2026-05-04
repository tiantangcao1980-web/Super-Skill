---
name: ai-agent-frameworks
description: 设计、实现、重构或排查 AI Agent 框架应用。Use when the task involves OpenClaw, LangGraph, AutoGen, AgentScope, CrewAI, Spring AI Alibaba, or similar tool-calling / multi-agent workflows.
---

# AI Agent 开发框架

## 框架全景与选型 (2026.02 最新)

| 框架 | 语言 | 最新版本 | 定位 | 适用场景 |
|------|------|----------|------|----------|
| OpenClaw | TypeScript | v2026.2.25 | 个人 AI 助手 | 多渠道(WhatsApp/Telegram/Slack/Synology)、语音、Android/iOS |
| Spring AI Alibaba | Java | v1.1.2.0 | 企业级 AI 集成 | Spring 生态、多Agent模式(routing/supervisor/handoffs)、通义千问 |
| AutoGen | Python | v0.7.4 | 多智能体协作 | 事件驱动编程、对话式 Agent 团队、代码生成 |
| AgentScope | Python | Runtime v1.1.0 | 灵活多智能体 | ReAct/Handoffs/Routing、分布式、长期记忆 |
| LangChain | Python/TS | 持续更新 | Agent 工程平台 | RAG、工具使用、LangSmith 可观测性 |
| CrewAI | Python | v1.9.0 | 角色扮演团队 | Flows 架构、A2A 协议、企业级追踪 |
| LangGraph | Python | v0.4+ | 状态图工作流 | Deferred Nodes、MCP 集成、LangGraph Platform |
| Dify | Python/TS | 持续更新 | 低代码 AI 平台 | 可视化编排、RAG、工作流、API 化 |
| Open-AutoGLM | Python | 实验阶段 | 端侧 Agent | 设备操作、屏幕理解、自主执行 |

### 最新趋势速览 (2026)
- **A2A 协议**: CrewAI 原生支持 Agent-to-Agent 通信标准
- **MCP 集成**: LangGraph/LangChain 全面支持 Model Context Protocol
- **多Agent模式内置**: Spring AI Alibaba v1.1.2 内置 routing/supervisor/handoffs/skills 模式
- **分布式中断**: AgentScope 支持分布式任务中断和原子状态机
- **事件驱动**: AutoGen v0.7 转向事件驱动编程模型

## 核心架构模式

### 1. ReAct 循环（推理 + 行动）

```python
"""
ReAct 模式 — 所有 Agent 框架的核心循环
"""
class ReActAgent:
    def __init__(self, llm, tools: list):
        self.llm = llm
        self.tools = {t.name: t for t in tools}

    def run(self, task: str) -> str:
        """思考-行动-观察循环"""
        history = [{"role": "user", "content": task}]

        for _ in range(10):  # 最大迭代次数
            # 思考: LLM 决定下一步
            response = self.llm.chat(history)

            if response.is_final_answer:
                return response.content

            # 行动: 调用工具
            tool = self.tools[response.tool_name]
            observation = tool.execute(response.tool_args)

            # 观察: 将结果加入历史
            history.append({"role": "assistant", "content": response.content})
            history.append({"role": "tool", "content": observation})

        return "达到最大迭代次数"
```

### 2. 多智能体协作模式

```python
"""
多 Agent 协作 — AutoGen/CrewAI/AgentScope 的核心模式
"""
class MultiAgentTeam:
    def __init__(self):
        self.agents = {}

    def add_agent(self, name: str, role: str, llm_config: dict):
        """添加具有特定角色的 Agent"""
        self.agents[name] = Agent(name=name, role=role, **llm_config)

    def run_conversation(self, task: str, max_rounds: int = 10):
        """Agent 间对话协作"""
        messages = [{"sender": "user", "content": task}]

        for round_num in range(max_rounds):
            for name, agent in self.agents.items():
                response = agent.respond(messages)
                messages.append({"sender": name, "content": response})

                if response.contains("TASK_COMPLETE"):
                    return self.summarize(messages)

        return self.summarize(messages)
```

### 3. 工具调用模式（Function Calling）

```python
"""
工具定义与调用 — LangChain/OpenClaw 通用模式
"""
from typing import Callable

class Tool:
    def __init__(self, name: str, description: str, func: Callable, schema: dict):
        self.name = name
        self.description = description  # LLM 用此决定是否调用
        self.func = func
        self.schema = schema            # 参数 JSON Schema

    def execute(self, **kwargs):
        """执行工具并返回结果"""
        try:
            return {"success": True, "result": self.func(**kwargs)}
        except Exception as e:
            return {"success": False, "error": str(e)}

# 注册工具示例
search_tool = Tool(
    name="web_search",
    description="搜索互联网获取最新信息",
    func=lambda query: search_engine.search(query),
    schema={"type": "object", "properties": {"query": {"type": "string"}}}
)
```

## 各框架快速上手

### OpenClaw (TypeScript)

```typescript
/**
 * OpenClaw — 个人 AI 助手
 * 支持 WhatsApp/Telegram/Slack/Discord 等多渠道
 */

// 配置 ~/.openclaw/openclaw.json
const config = {
  agent: {
    model: "anthropic/claude-opus-4-6",
  },
  channels: {
    telegram: { botToken: "YOUR_TOKEN" },
  },
};

// 自定义 Skill
// ~/.openclaw/workspace/skills/my-skill/SKILL.md
```

核心概念 (v2026.2):
- **Gateway**: WebSocket 控制面板，管理会话/渠道/工具
- **Pi Agent**: RPC 模式的 AI 运行时，默认使用 Claude Opus 4.6
- **Skills**: 可安装的能力模块
- **Nodes**: 设备节点（macOS/iOS/Android/Synology）
- **Providers**: 支持 Kilo/Mistral/Moonshot 等多供应商

### Spring AI Alibaba (Java)

```java
/**
 * Spring AI Alibaba — 企业级 AI 应用框架
 * 集成通义千问、向量存储、RAG
 */
@RestController
public class ChatController {

    private final ChatClient chatClient;

    public ChatController(ChatClient.Builder builder) {
        this.chatClient = builder
            .defaultSystem("你是一个专业的技术助手")
            .build();
    }

    /** 对话接口 */
    @GetMapping("/chat")
    public String chat(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .call()
            .content();
    }

    /** 带工具调用的对话 */
    @GetMapping("/chat-with-tools")
    public String chatWithTools(@RequestParam String message) {
        return chatClient.prompt()
            .user(message)
            .functions("searchDatabase", "sendEmail")
            .call()
            .content();
    }
}

// application.yml 配置
// spring.ai.dashscope.api-key: ${DASHSCOPE_API_KEY}
// spring.ai.dashscope.chat.options.model: qwen-max
```

核心概念 (v1.1.2):
- **ChatClient**: 统一的对话客户端
- **ReactAgent**: 内置 Agent Skills 支持
- **Flow Agent**: 支持 routing/supervisor/loop/sequential 等多Agent模式
- **Function Calling**: 异步+并行工具执行，支持 returnDirect
- **VectorStore**: 向量存储（RAG）
- **streamMessages**: 简化的流式消息 API

### AutoGen (Python)

```python
"""
AutoGen — 微软多智能体框架
"""
import autogen

# 定义 Agent
assistant = autogen.AssistantAgent(
    name="编程助手",
    llm_config={"model": "gpt-4o"},
    system_message="你是一个高级程序员，擅长 Python 和系统设计。"
)

code_reviewer = autogen.AssistantAgent(
    name="代码审查员",
    llm_config={"model": "gpt-4o"},
    system_message="你负责审查代码质量和安全性。"
)

user_proxy = autogen.UserProxyAgent(
    name="用户代理",
    human_input_mode="NEVER",
    code_execution_config={"work_dir": "workspace"},
)

# 启动群聊协作
groupchat = autogen.GroupChat(
    agents=[user_proxy, assistant, code_reviewer],
    messages=[], max_round=12
)
manager = autogen.GroupChatManager(groupchat=groupchat)
user_proxy.initiate_chat(manager, message="实现一个 REST API 用户认证模块")
```

### AgentScope (Python)

```python
"""
AgentScope — 灵活的多智能体框架
支持自定义拓扑、分布式部署
"""
import agentscope
from agentscope.agents import DialogAgent
from agentscope.pipelines import SequentialPipeline

# 初始化
agentscope.init(model_configs=[{
    "model_type": "dashscope_chat",
    "config_name": "qwen",
    "model_name": "qwen-max",
}])

# 创建 Agent
architect = DialogAgent(
    name="架构师",
    sys_prompt="你是一个资深系统架构师",
    model_config_name="qwen",
)

developer = DialogAgent(
    name="开发者",
    sys_prompt="你是一个全栈开发工程师",
    model_config_name="qwen",
)

# 流水线式协作
pipeline = SequentialPipeline([architect, developer])
result = pipeline({"content": "设计一个微服务电商系统"})
```

### LangChain / LangGraph (Python)

```python
"""
LangGraph — 有状态 Agent 工作流
"""
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    next_step: str

def research_node(state: AgentState) -> AgentState:
    """研究节点 — 收集信息"""
    # 调用搜索工具
    return {"messages": state["messages"] + [result], "next_step": "analyze"}

def analyze_node(state: AgentState) -> AgentState:
    """分析节点 — 处理信息"""
    return {"messages": state["messages"] + [analysis], "next_step": "report"}

# 构建状态图
graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("analyze", analyze_node)
graph.add_edge("research", "analyze")
graph.add_edge("analyze", END)

app = graph.compile()
result = app.invoke({"messages": ["调研 AI Agent 框架趋势"], "next_step": "research"})
```

## 框架复用与重构策略

### 通用抽象层

```python
"""
统一 Agent 接口 — 屏蔽框架差异
"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Agent 统一抽象，可适配不同框架"""

    @abstractmethod
    def chat(self, message: str) -> str:
        """单轮对话"""

    @abstractmethod
    def chat_with_tools(self, message: str, tools: list) -> str:
        """带工具调用的对话"""

    @abstractmethod
    def stream(self, message: str):
        """流式输出"""

class LangChainAdapter(BaseAgent):
    """LangChain 适配器"""
    def __init__(self, chain):
        self.chain = chain

    def chat(self, message: str) -> str:
        return self.chain.invoke(message)

class AutoGenAdapter(BaseAgent):
    """AutoGen 适配器"""
    def __init__(self, agent):
        self.agent = agent

    def chat(self, message: str) -> str:
        return self.agent.generate_reply([{"content": message, "role": "user"}])
```

### 迁移与重构检查清单

- [ ] 识别框架特有 API vs 通用逻辑
- [ ] 提取 Prompt Template 为独立文件
- [ ] 工具定义标准化（OpenAI Function Calling 格式）
- [ ] 记忆/上下文管理统一接口
- [ ] 配置外部化（环境变量 / 配置文件）
- [ ] 错误处理和重试逻辑统一

## MCP 协议与 Agent 集成

MCP (Model Context Protocol) 是连接 Agent 与外部工具/数据的标准协议：

```json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

### 开发自定义 MCP 服务器

```python
"""
自定义 MCP 服务器模板
"""
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("my-agent-tools")

@app.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_knowledge",
            description="搜索知识库",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_knowledge":
        results = knowledge_base.search(arguments["query"])
        return [TextContent(type="text", text=str(results))]
```

## 选型决策指南 (2026 版)

| 需求 | 推荐框架 | 理由 |
|------|----------|------|
| 个人助手 + 多渠道 | OpenClaw | 最全渠道支持，370+ 贡献者活跃社区 |
| Java 企业应用 | Spring AI Alibaba | Spring 生态深度集成，内置多Agent模式 |
| 多 Agent 研究协作 | AutoGen | 事件驱动架构，微软支持 |
| 灵活拓扑 + 国产模型 | AgentScope | 分布式原生，阿里达摩院出品 |
| 快速原型 + RAG | LangChain | 最大生态，LangSmith 可观测 |
| 企业 Agent 团队 | CrewAI | A2A 协议，Flows 生产架构，企业级追踪 |
| 复杂有状态工作流 | LangGraph | MCP 原生，Deferred Nodes，Platform GA |
| 低代码/可视化 | Dify | 拖拽式编排，快速部署 |
| 端侧自主操作 | Open-AutoGLM | 设备操控，屏幕理解 |

## 获取最新信息

使用 context7 MCP 查询任意框架的最新文档：
```
resolve-library-id → query-docs
```
使用 fetch MCP 查看 GitHub releases：
```
fetch https://github.com/<org>/<repo>/releases
```
