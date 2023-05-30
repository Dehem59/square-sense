# INSTALLATION
- make python virtual environment
- activate it
- install dependencies with "pip install -r requirements.txt"
- run webserver with flask runapp command or through IDE

# ARCHITECTURE
## core app
- DAO (data access object) layer to interact with a storage: In Memory, JSON, SQL ...
- Repository that manages records with some business logic and model transformation / validation
- Model that represents an unitary entity storing the data
- settings module is a runtime configuration
## web app
- the web app contains the Flask configuration for endpoints and serializer to validate data (dict --> to python)

## tests module
unit test module