from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ShoppingCrew:
    """Shopping Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=self.api_key)

    @agent
    def products_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["products_manager"],
            llm=self.llm
        )

    @agent
    def customer_support(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_support"],
            llm=self.llm
        )

    @task
    def manager_task(self) -> Task:
        return Task(
            config=self.tasks_config["manager_task"],
        )

    @task
    def customer_task(self) -> Task:
        return Task(
            config=self.tasks_config["customer_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Shopping Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )