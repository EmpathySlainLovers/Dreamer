# Dreamer AI

A basic AI assistant app to be developed and deployed.

## How to Run Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set the `OPENAI_API_KEY` environment variable in your shell or in a `.env` file.
3. Start the app:
   ```bash
   python app.py
   ```

## Using `termux_chatgpt.py` in Termux

1. Install Python and Git in Termux:
   ```bash
   pkg install python git
   ```
2. Clone this repository and install the dependencies:
   ```bash
   git clone <repository-url>
   cd Dreamer
   pip install -r requirements.txt
   ```
3. Export your API key:
   ```bash
   export OPENAI_API_KEY=your-key
   ```
4. Run the script:
   ```bash
   python termux_chatgpt.py
   ```

Commands beginning with `!` inside the program will be executed directly in the Termux shell and the output will be printed.
