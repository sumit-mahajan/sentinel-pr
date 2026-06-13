from enum import Enum


class AgentType(str, Enum):
    SECURITY = "security"
    PERF = "perf"
    ARCH = "arch"
    TEST = "test"
