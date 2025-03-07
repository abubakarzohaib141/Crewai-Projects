import os
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from poem_crew import ShoppingCrew  # Assuming poem_crew.py contains ShoppingCrew definition
import streamlit as st

# Initialize session state for memory
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Enter your shopping query:")

class ShoppingState(BaseModel):
    answer: str = ""
    history: list = [] # Add history to state

class ShoppingFlow(Flow[ShoppingState]):

    @start()
    def start_development(self):
        print("Starting Flow")
        self.state.history = st.session_state.chat_history # load history from session
            # if user_input:
            #     self.generate_answer()

    @listen(start_development)
    def generate_answer(self):
        print("Getting Alll Things Ready ......")
        # Convert history list to string
        history_str = "\n".join([f"User: {item['user']}\nAgent: {item['agent']}" for item in self.state.history])
        input_data = {"input": user_input, "history": history_str} #pass the string
        result = (
            ShoppingCrew()
            .crew()
            .kickoff(inputs=input_data)
        )
        st.title("Shop Hop")
        st.write("Shopping Agent : ", result.raw)
        print("Shopping Agent : ", result.raw)
        self.state.answer = result.raw
        # self.state.history.append({"user":user_input, "agent": result.raw}) #update history
        # st.session_state.chat_history = self.state.history # save history to session
        # self.display_chat_history() #display after update.

    @listen(generate_answer)
    def save_poem(self):
        print("Saving Answer")
        with open("shopping_agent.txt", "w") as f:
            f.write(self.state.answer)

    def display_chat_history(self):
        for message in st.session_state.chat_history:
            st.write(f"User: {message['user']}")
            st.write(f"Agent: {message['agent']}")

def kickoff():
    shopping_flow = ShoppingFlow()
    shopping_flow.kickoff()

def plot():
    shopping_flow = ShoppingFlow()
    shopping_flow.plot()

if __name__ == "__main__":
    kickoff()
