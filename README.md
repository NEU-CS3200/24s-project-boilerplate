## Project Overview:

Our project aims to create a comprehensive scheduling application using the AppsSmith platform. The UI is customized to meet the scheduling needs of owners, employees, and managers within a business context. By leveraging AppSmith's capabilities, we provide a streamlined and intuitive scheduling solution tailored for different organizational roles.


-------------------------------------------------------------------------------

## Key Features of Personas:
- Owner
  -  Can access locations using a GET.
  -  Allowed to pull information about specific shifts using a GET.
    
- Employee
  - Employees are permitted to request time off with a POST route.
  - Able to view their schedules via a GET.

- Manager
  - Allowed to access the information of other managers' schedule information via a GET.
  - Managers can view all employees/users, choose one, and delete them using a DELETE route from the database.
  - Can access a table of all employee's tasks using a GET.
  - Able to edit an employee's role via a PUT route.
 
-------------------------------------------------------------------------------



## Getting Started:

To use the AppSmith UI for scheduling purposes, here are the following steps:

1.) Clone the repository to your local machine

    git clone https://github.com/Airelyn/24s-project-boilerplate
2.) Navigate to project directory

    cd 24s-project-boilerplate
3.) Start docker containers using docker-compose

    docker-compose up -d
4.) Access the application. Once the containers are running, access the application through your web browser

    - OWNER: HTTP://localhost:8080/owner
    - EMPLOYEE: HTTP://localhost:8080/employee
    - MANAGER: HTTP://localhost:8080/manager
5.) Refer to the Docker Compose file ('docker-compose.yml) to adjust environment variables or container settings as needed.


-------------------------------------------------------------------








c/Users/airelynguadagno/Desktop/3200-practice/24s-project-boilerplate/docker-compose.yml# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




