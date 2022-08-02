# Clone repository
`git clone https://github.com/razorblade23/FlaskAdminSchoolProject.git`
### cd into a folder where you cloned repository

# Build a new virtual env
`python -m venv venv`

# Activate virtual env
### Windows

`venv/Scripts/activate.ps1`

### Linux

`source venv/bin/activate`


# Download and install requirements

`pip install -r requirements.txt`


# Create a database
### This will also generate:
 - 1 admin account
    -- username: root23
    -- password: same as username
 - 10 user accounts with fake data
    -- username and password is the same
 - 50 fake companies to test the app

`python build_db.py`

# Run run.py to start application
`python run.py`

## This runs on localhost:5000 (default)
