from crewai import Agent
from pbq.generator import PBQGenerator, PBQContext


def create_pbq_agent(llm_client):
    """
    PBQ Agent: Generates SC-300 PBQs using the PBQGenerator module.
    """

    return Agent(
        role="PBQ Generator Agent",
        goal=(
            "Generate Microsoft SC-300 style Performance-Based Questions (PBQs) "
            "based on the scenario context and chain outputs."
        ),
        backstory=(
            "You specialize in transforming IAM/PIM/PAM/Governance/Compliance "
            "analysis into exam-ready PBQs that follow strict JSON structure."
        ),
        llm=llm_client,
        allow_delegation=False,
        verbose=True,
    )
