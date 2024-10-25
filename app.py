import os
import gradio as gr
from interpreter import interpreter
import argparse
import subprocess
import sys
import shlex

# Fetch the Hugging Face API key from environment variables
api_key = os.getenv("HUGGINGFACE_API_KEY")

if not api_key:
    raise ValueError("API key not found. Set the HUGGINGFACE_API_KEY environment variable.")

# Set the API key for the interpreter
interpreter.llm.api_key = api_key
interpreter.llm.model = "meta-llama/Llama-3.1-8B-Instruct"  # Example model

# Function to execute shell commands if detected in model output
def execute_shell_command(command):
    # Sanitize user input using shlex.split to avoid security vulnerabilities
    sanitized_command = shlex.split(command)
    result = subprocess.run(sanitized_command, capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else result.stderr

# Function to process tasks using OpenInterpreter and detect shell commands
def execute_task(task):
    try:
        # Get the model-generated response first
        response = interpreter.chat(task)
    except Exception as e:
        return f"Error while interacting with the model: {str(e)}"
    
    # Check if the response indicates a shell command
    if "run shell" in response.lower():
        command = response.split("run shell", 1)[1].strip()
        return execute_shell_command(command)
    else:
        return response

# CLI interface using argparse
def cli_interface():
    parser = argparse.ArgumentParser(description="Command-line interaction with OpenInterpreter.")
    parser.add_argument("--task", type=str, required=True, help="The task or command to execute")
    args = parser.parse_args()

    # Execute the task and print the result
    result = execute_task(args.task)
    print(result)

# Main entry point for the script
if __name__ == "__main__":
    # Run the CLI interface only, no web app
    cli_interface()
