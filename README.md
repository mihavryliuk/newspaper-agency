
# newspaper_agency

App for newspaper agency to create new newspapers

to try:
username = user;  
password = userpass321

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mihavryliuk/newspaper-agency
   cd newspaper_agency
   
2. **Create and activate a virtual environment:**
   ```bash
    python -m venv .venv
    .venv\Scripts\activate

3. **Install dependencies**
   ```bash
    pip install -r requirements.txt
4. **Create a .env file from the sample**
    ```bash
    cp .env.sample .env

5. **Run database migrations**
    ```bash
    python manage.py migrate
6. **Run server**
    ```bash
    python manage.py runserver

   

## deployed to

https://newspaper-agency-96fn.onrender.com

```To populate db
python manage.py loaddata data1.json

```


## Features


* Register redactors
* Add newspapers
* Create new topics



## Contributing



"If you'd like to contribute, please fork the repository and use a feature
branch. Pull requests are warmly welcome."


## Links

Even though this information can be found inside the project on machine-readable
format like in a .json file, it's good to include a summary of most useful
links to humans using your project. You can include links like:

- Project homepage: https://github.com/mihavryliuk/newspaper-agency
