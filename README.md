# AI Researcher Test

## Dependencies

- Python 3.12
- Poetry 1.7.1


## Useful Commands

- `make start` - run the main app
- `make install` - install dependencies
- `make format` - run formatters
- `make lint` - run linting


### Local Dev Setup

#### PyCharm

- Code Formatting on save
  - Newer PyCharms:
    - Settings -> Tools -> Black -> enable "On Code Reformat" and "On Save" 
  - Older PyCharms: 
    - Install BlackConnect plugin
    - Run `poetry run blackd`
    - Enable "Trigger when saving file" in plugin settings


## Archive

### Original Installation Steps

- Install python 3.12 (using pyenv or by another way)
- Install pipx (npx equivalent)
  - Follow steps for your OS here: [https://github.com/pypa/pipx](https://github.com/pypa/pipx)
- Install Poetry (yarn equivalent)
  - `pipx install poetry`
- Install Dev Tools
  - `poetry add --dev black`
  - `poetry add --dev isort`
  - `poetry add --dev flake8`
- Install Libs
  - `poetry add openai`
  - `poetry add langchain`
  - `poetry add python-dotenv`
