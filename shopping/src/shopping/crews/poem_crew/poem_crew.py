from crewai import Agent, Crew, Process, Task , LLM
from crewai.project import CrewBase, agent, crew, task
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

os.environ["GEMINI_API_KEY"] = "AIzaSyAl7RtHDwkiOdw3iw1GY1wW7EKHjGFqEAI"

llm = LLM(model = "gemini/gemini-2.0-flash-exp")

@CrewBase
class ShoppingCrew:
    """Shopping Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def products_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["products_manager"],
            llm = llm
        )    
    @agent
    def customer_support(self) -> Agent:
        return Agent(
            config=self.agents_config["customer_support"],
            llm = llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
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
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
