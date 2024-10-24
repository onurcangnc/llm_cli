import os
import gradio as gr
from interpreter import interpreter
import argparse
import subprocess
import sys

# Fetch the Hugging Face API key from environment variables
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set the HUGGINGFACE_API_KEY environment variable.")

# Set the API key for the interpreter
interpreter.llm.api_key = api_key
interpreter.llm.model = "meta-llama/Llama-3.1-8B-Instruct"  # Example model

# Function to execute tasks using OpenInterpreter
def execute_task(task):
    if task.startswith("run shell"):
        command = task.replace("run shell", "").strip()
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    else:
        return interpreter.chat(task)

# CLI interface using argparse
def cli_interface():
    parser = argparse.ArgumentParser(description="Command-line interaction with OpenInterpreter.")
    parser.add_argument("--task", type=str, required=True, help="The task or command to execute")
    args = parser.parse_args()

    # Execute the task and print the result
    result = execute_task(args.task)
    print(result)

# Gradio interface for the web app
def run_gradio_interface():
    iface = gr.Interface(fn=execute_task, inputs="text", outputs="text")
    iface.launch()

# Main entry point for the script
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run the CLI if arguments are provided
        cli_interface()
    else:
        # Run the Gradio web app by default
        run_gradio_interface()
