from __future__ import annotations

from .contracts import AgentResponse, QueryPlan, UserRequest
from .data_prep import DataPrepAgent
from .rag import SimpleRAGStore
from .sql_tools import SQLIntegrationAgent
from .tableau import TableauDashboardAgent, TableauPayloadValidator


class LIOrchestratorAgent:
    """Natural-language orchestrator for SQL -> data prep -> Tableau output."""

    def __init__(self, db_path: str, knowledge_base_path: str) -> None:
        self.sql_agent = SQLIntegrationAgent(db_path)
        self.prep_agent = DataPrepAgent()
        self.rag = SimpleRAGStore(knowledge_base_path)
        self.tableau_agent = TableauDashboardAgent(TableauPayloadValidator())

    def run(self, request: UserRequest) -> AgentResponse:
        self.sql_agent.setup_demo_data()

        plan = QueryPlan(
            steps=[
                "sql-integration: query warehouse",
                "data-prep: clean and normalize rows",
                "tableau-dashboard: generate validated payload",
                "reporting: return terminal summary",
            ],
            metadata={"mode": "short_term_scaffold", "request": request.prompt},
        )

        data = self.sql_agent.query("SELECT region, segment, sales, profit FROM sales")
        prepared = self.prep_agent.clean(data)

        docs = self.rag.retrieve(request.prompt, top_k=2)
        dashboard = self.tableau_agent.build_payload(
            prompt=request.prompt,
            datasource="sqlite.sales",
            available_columns=list(prepared.schema.keys()),
            knowledge_docs=docs,
        )

        report = (
            "Generated dashboard payload with validated fields. "
            f"Rows processed: {len(prepared.rows)}. "
            f"Knowledge docs used: {len(docs)}."
        )

        return AgentResponse(plan=plan, data=prepared, dashboard=dashboard, report=report)
