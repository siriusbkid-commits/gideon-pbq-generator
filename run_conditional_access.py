from crewai import Crew
from agents import conditional_access_evaluator
from tasks import evaluate_conditional_access_task

# Attach agent to task
evaluate_conditional_access_task.agent = conditional_access_evaluator

# Build the crew
ca_crew = Crew(
    agents=[conditional_access_evaluator],
    tasks=[evaluate_conditional_access_task]
)

# Run the workflow
result = ca_crew.kickoff()
print(result)
