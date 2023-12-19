# AI Researcher Test

## Dependencies

- Python 3.10.5
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

### Environment Installation Steps

- Install pyenv
  - Follow steps for Windows here: [https://github.com/pyenv-win/pyenv-win](https://github.com/pyenv-win/pyenv-win)
- Install python 3.10
  - `pyenv install 3.10.5`
  - `pyenv local 3.10.5`
- Install pipx (npx equivalent)
  - `scoop install pipx`
  - Or follow steps for your OS here: [https://github.com/pypa/pipx](https://github.com/pypa/pipx)
- Install Poetry (yarn equivalent)
  - `pipx install poetry`
- `poetry install`
