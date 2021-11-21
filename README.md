# Simple Blog App with Flask

This is a simple Blog App created with Flask.

## Getting Started

### Prerequisites

Python3 and Pip3 need to be installed on your system.

### Installing the dependencies

The following command installs all required dependencies:

```
pip install -r requirements.txt
```

### Creating the database

The following commands create the database:

-   start up python3 interpreter:

```
python3
```

-   execute the following commands:

```
from blog_app import create_app, db
app = create_app()
db.create_all(app=app)
```

### Starting the application

The following command starts up the appliation:

```
FLASK_APP=blog_app flask run
```

## Author

-   **Stefan Eyerer**
