from crewai import Crew
from tasks import test_task

test_crew = Crew(
    tasks=[test_task],
    verbose=True
)
