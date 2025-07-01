# Dreamer AI

A basic AI assistant app to be developed and deployed.

## How to Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Using `termux_chatgpt.py`

1. Ensure the `openai` Python package is installed (it's included in `requirements.txt`).
2. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the assistant in Termux:

   ```bash
   python termux_chatgpt.py
   ```

Commands starting with `!` will be executed in the Termux shell.
