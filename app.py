import os
import gradio as gr
from interpreter import interpreter

# Fetch the Hugging Face API key from environment variables
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set the HUGGINGFACE_API_KEY 
environment variable.")

# Set the API key for the interpreter
interpreter.llm.api_key = api_key
interpreter.llm.model = "meta-llama/Llama-3.1-8B-Instruct"  # Example 
model

# Function to execute tasks using OpenInterpreter
def execute_task(task):
    result = interpreter.chat(task)  # This executes the task using the 
specified model
    return result

# Gradio interface to interact with the interpreter
iface = gr.Interface(fn=execute_task, inputs="text", outputs="text")

# Launch the Gradio app
iface.launch()

