from crewai import Crew
from agents import identity_threat_analyst
from tasks import evaluate_signin_task

# Attach the agent to the task
evaluate_signin_task.agent = identity_threat_analyst

# Build the crew
iam_crew = Crew(
    agents=[identity_threat_analyst],
    tasks=[evaluate_signin_task]
)

# Run the workflow
result = iam_crew.kickoff()
print(result)
