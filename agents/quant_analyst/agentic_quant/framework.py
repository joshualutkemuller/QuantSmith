"""Core framework utilities for building agentic quantitative workflows."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Iterator, Protocol, Sequence


class Agent(Protocol):
    """Protocol representing an autonomous component in the workflow."""

    name: str

    def run(self, blackboard: "Blackboard") -> None:
        """Execute the agent and store its outputs on the shared blackboard."""


@dataclass
class Blackboard:
    """A lightweight blackboard used for agent coordination."""

    _data: Dict[str, Any] = field(default_factory=dict)

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def require(self, *keys: str) -> None:
        """Ensure that a set of keys is present on the blackboard."""

        missing = [key for key in keys if key not in self._data]
        if missing:
            raise KeyError(f"Blackboard missing required keys: {', '.join(missing)}")

    def items(self) -> Iterable[tuple[str, Any]]:
        return self._data.items()

    def as_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the stored data."""

        return dict(self._data)


class AgentPipeline:
    """Simple sequencer that runs a collection of agents in order."""

    def __init__(self, agents: Sequence[Agent]):
        if not agents:
            raise ValueError("agents must contain at least one agent")
        self._agents: list[Agent] = list(agents)

    def __iter__(self) -> Iterator[Agent]:
        return iter(self._agents)

    @property
    def agents(self) -> list[Agent]:
        """Expose the underlying agent list for inspection or mutation."""

        return self._agents

    def append(self, agent: Agent) -> None:
        """Append an agent to the end of the pipeline."""

        self._agents.append(agent)

    def run(self, blackboard: Blackboard | None = None) -> Blackboard:
        board = blackboard or Blackboard()
        for agent in self._agents:
            agent.run(board)
        return board
