from pydantic import BaseModel, Field
from uuid import UUID

class ChatMessage(BaseModel):
    role: str
    content: str = Field(max_length=12000)

class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)
    session_id: UUID | None = None

class AgentChatResponse(BaseModel):
    reply: str
    model: str
    tool_calls: list[dict]
    agent_type: str
    memory_mode: str
    tool_limit_reached: bool = False
    sensor_attached: bool = False
    token_efficiency: dict = Field(default_factory=dict)
    session_id: UUID | None = None
