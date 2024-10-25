import argparse
import gradio as gr
import torch
from transformers import pipeline

# Load the model
generator = pipeline("text-generation", model="gpt-neo-2.7B")

# Define a function to handle input and generate text
def generate_text(prompt):
    return generator(prompt, max_length=100, do_sample=True)[0]["generated_text"]

# CLI interface using argparse
def cli_interface():
    parser = argparse.ArgumentParser(description="Command-line interaction with the text generation model.")
    parser.add_argument("--task", type=str, help="The prompt or command to generate text for")
    args = parser.parse_args()

    # Provide a default task if none is provided
    task = args.task if args.task else "Tell me a joke"

    # Generate and print the result
    result = generate_text(task)
    print(result)

if __name__ == "__main__":
    cli_interface()

# Set up Gradio interface
interface = gr.Interface(fn=generate_text, inputs="text", outputs="text")

# Launch the app
interface.launch()
