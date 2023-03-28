# Rooms Scheduler App with Flask


## About
This project implements a app to manage the scheduling of rooms to have more control over scheduling and room's keys.

We developed this app as requested for the Software Arch discipline of the BSI graduation course.
This course is offered by IFNMG Campus Januária.

### Project Specification
- Apply the concepts of Clean Arch
- ...

**Obs:** This is a simple app, some features, errors and security threatments may be not available.


## Technologies
The app is containerized with Docker, and the features are developed using React and Flask to provide the APIs

- Docker
- Docker-compose

**Back-end**
- Python
- Flask Framework 

**Database**
- Postgresql


## How to Set-up the project

**Requirements:**
- Docker and Docker-compose must be installed in your local machine
- Is prefered to run this app in Linux envrioment (also can be Windows WSL)

**How to run**
- Clone this repository: `git clone https://github.com/bernardoadribeiro/rooms_scheduler_app`
- Go to project folder: `cd rooms_scheduler_app`
- Create the `.env` file: `cp .env.sample .env` (do it for the `.env.sample` in root and backend folders)
- (open Docker Desktop before continue if you are using WSL)
- Run: `docker-compose up` and wait.
- You will see a success message in the terminal

**Migrations**
> - Run the following lines when needs to manage migrations:
> - Usage: `flask db [OPTIONS] COMMAND [ARGS]...`

- `flask db init`: to create a folder with set to migration.
- `flask db migrate -m "Initial migration."`: to generate a migration.
- `flask db [upgrade|downgrade]`: to up/down changes based on migration files.
- `flask db --help`: Show database help message.

**How to access the app**
- Back-end URL: http://127.0.0.1:5000/api/v1
- APIs docs (Swagger): `TO-DO`

**Useful commands**
- `docker-compose up`: Run all containers
- `docker-compose down`: Stop all containers
- `docker-compose build [backend | frontend | database]`: Re-build a specific container
- Install React dependencies: `cd frontend && npm install`
- `$ flask create-db`
- `$ flask populate-db`
- `$ flask add-user -u <digite um usuário> -p <digite uma senha>`


## Project Structure
```

```