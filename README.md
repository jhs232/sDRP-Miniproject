# Requirements:

- `python3`
- `docker`


# Setup

1. Install requirements
2. Create a virtual environment, e.g. directly within this folder: `python -m venv .venv` (destination is .venv within the current dir).
3. Activate the virtual environment `source .venv\bin\activate` (source is different if you didn't use the .venv destination)
4. Install requirements from requirements.txt: `python -m pip install -r requirements.txt` (must be run from the folder where requirements.txt is)
5. Start docker containers `sudo docker-compose up -d`

# Usage
Use the `db.py` file which contains connection parameters matching with the docker-compose project. You 
