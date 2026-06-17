# commitmessagegenerator

Generate objective and technical commit messages with AI (Google Gemini) automatically using your `git diff`.

## 📦 Install

```bash
pip install commitmessagegenerator
```

Or, if you're using a `venv`:

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate in Windows
pip install commitmessagegenerator
```

## ⚙️ Configuring

```bash
commitgen -cf
```

You can explicitly choose where configuration is written:

```bash
commitgen -cf --config-scope auto    # default behavior
commitgen -cf --config-scope local   # always write .env in current directory
commitgen -cf --config-scope global  # always write ~/.commitgen/.env
```

This opens an interactive configuration menu where you can:

1. Set or update your Gemini API key
2. Change the AI model
3. Configure file staging behavior

Each option can be configured independently, and you can exit at any time without saving changes.

## Run this and type you API key to the terminal so the package creates the .env file and automatically adds it to the .gitignore

Or do it manually:

## IMPORTANT - BEFORE CREATING THIS FILE ADD '.venv' TO YOUR .gitignore SO YOUR API KEY ISN'T EXPOSED

Create a `.env` file in the directory where you will run commitgen (usually the root of your Git project):

```
GEMINI_API_KEY=your-gemini-api-key
AI_MODEL=gemini-2.5-flash
AUTO_ADD_ALL=true
```

Config discovery order:

1. `.env` in current directory
2. `.env` in parent directories (useful when running from subfolders)
3. Global config in `~/.commitgen/.env` (created automatically by `commitgen -cf --config-scope auto` when no local `.env` exists)

Environment variables already set in your shell (e.g. `GEMINI_API_KEY`) are also respected.

## 🚀 Usage

With the terminal, inside any Git repository with pending changes, run:

```bash
commitgen (-c/-cp)
```

The command will:

- Read the git diff;
- Send it to the Google Gemini API using your configured model;
- Return a commit message suggestion directly in your terminal.

### Available Commands

- `commitgen` - Generate commit message only
- `commitgen -c` - Generate and commit with the message
- `commitgen -cp` - Generate, commit, and push
- `commitgen -cf` - Configure API key, model, and file staging behavior
- `commitgen -cf --config-scope [auto|local|global]` - Choose where `.env` is created/updated
- `commitgen -s` - Show current configuration status

### Available Models

When configuring with `-cf`, you can choose from:

1. **gemini-2.5-flash** (default) - Fast and efficient, best price-performance
2. **gemini-2.5-flash-lite** - Fastest and most economical
3. **gemini-2.5-pro** - Advanced reasoning and coding
4. **gemini-3-flash** - Frontier performance (preview)
5. **gemini-3.5-flash** - Latest stable model, best for coding
6. **gemini-3.1-pro** - Highest quality (preview)

### File Staging Behavior

When configuring with `-cf`, you can choose how files are staged:

1. **Auto-add all files** (default) - Automatically runs `git add --all` before generating the commit message
2. **Staged only** - Only reads the diff from files you've already staged with `git add`

The "staged only" option gives you more control over which changes are included in the commit message.

## 🧩 Requisites

- Python 3.8 or higher
- Gemini API Key (Google Generative AI, free at: https://aistudio.google.com/app/apikey)
- Initialized Git repository
- Python dependencies (Automatically installed with the package):
  - `GitPython`
  - `google-generativeai`
  - `python-dotenv`

## 📄 License

```
MIT License
```
