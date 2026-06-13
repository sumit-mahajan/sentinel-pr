"""
LangGraph StateGraph for the multi-agent review pipeline.

Flow:
  START → supervisor → fan-out to active agents (parallel) → synthesis → END

Each node is a pure state transformer that receives ReviewState and returns ReviewState.
"""
from __future__ import annotations

from typing import Literal

from langgraph.graph import END, START, StateGraph

from domain.value_objects.agent_type import AgentType
from infrastructure.ai.agents.arch_agent import ArchAgent
from infrastructure.ai.agents.perf_agent import PerfAgent
from infrastructure.ai.agents.security_agent import SecurityAgent
from infrastructure.ai.agents.supervisor_agent import SupervisorAgent
from infrastructure.ai.agents.synthesis_agent import SynthesisAgent
from infrastructure.ai.agents.test_agent import TestAgent
from infrastructure.ai.graph.state import ReviewState


def build_review_graph(
    supervisor: SupervisorAgent,
    security: SecurityAgent,
    perf: PerfAgent,
    arch: ArchAgent,
    test: TestAgent,
    synthesis: SynthesisAgent,
) -> StateGraph:
    graph = StateGraph(ReviewState)

    # Register nodes
    graph.add_node("supervisor", supervisor.run)
    graph.add_node("security", security.run)
    graph.add_node("perf", perf.run)
    graph.add_node("arch", arch.run)
    graph.add_node("test", test.run)
    graph.add_node("synthesis", synthesis.run)

    # START → supervisor
    graph.add_edge(START, "supervisor")

    # supervisor → conditional fan-out to active agents
    def route_from_supervisor(state: ReviewState) -> list[str]:
        agent_map = {
            AgentType.SECURITY: "security",
            AgentType.PERF: "perf",
            AgentType.ARCH: "arch",
            AgentType.TEST: "test",
        }
        return [agent_map[a] for a in state.get("active_agents", []) if a in agent_map]

    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        ["security", "perf", "arch", "test"],
    )

    # All specialist agents → synthesis
    for node in ["security", "perf", "arch", "test"]:
        graph.add_edge(node, "synthesis")

    # synthesis → END
    graph.add_edge("synthesis", END)

    return graph
