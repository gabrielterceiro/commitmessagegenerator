import os
from dotenv import load_dotenv
from google import genai
from git import Repo
from .configure import get_configured_model, get_auto_add_setting

def gerar_mensagem_commit():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set.")

    # Get the configured model
    model = get_configured_model()

    client = genai.Client(api_key=key)
    

    repo = Repo(os.getcwd())

    # Check if auto-add is enabled
    auto_add = get_auto_add_setting()
    if auto_add:
        # Automatically stage all changes
        repo.git.add(all=True)
    
    diff = repo.git.diff("--cached")

    if not diff.strip():
        return "No changes detected in staged files (git diff --cached). No commit message generated."

    prompt = (
        f'''
        Generate a technical and concise Git commit message in plain text format.

        The message should follow the standard convention:
        - A single subject line (50 characters max) in the imperative mood, summarizing the change.
        - An optional blank line followed by a body explaining the *what* and *why* of the change (72 characters per line max).

        Provide *only* the commit message text, ready for direct insertion into a commit. Do not include any conversational text or additional formatting.

        Based on the following changes: {diff}
        '''
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text.strip() if response.text else "Failed to generate commit message"