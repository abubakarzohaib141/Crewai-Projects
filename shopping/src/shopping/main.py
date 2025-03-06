import os


# Temporarily comment out the rest of the code
# class ShoppingCrew:
#     ...
#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from shopping.crews.poem_crew.poem_crew import ShoppingCrew

user_input = input("You : ")

class ShoppingState(BaseModel):
    answer: str = ""

class ShoppingFlow(Flow[ShoppingState]):

    @start()
    def start_development(self):
        print("Starting Flow")
      
          

    @listen(start_development)
    def generate_answer(self):
        print("Getting Alll Things Ready ......")
        result = (
            ShoppingCrew()
            .crew()
            .kickoff(inputs={"input": user_input})
        )   
        
        print("Shopping Agent : ", result.raw)
        self.state.answer = result.raw

    @listen(generate_answer)
    def save_poem(self):
        print("Saving Answer")
        with open("shopping_agent.txt", "w") as f:
            f.write(self.state.answer)


def kickoff():
    shopping_flow = ShoppingFlow()
    shopping_flow.kickoff()


def plot():
    shopping_flow = ShoppingFlow()
    shopping_flow.plot()


if __name__ == "__main__":
    kickoff()
