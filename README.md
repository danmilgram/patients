# Patient registration system

- Overview:
    This API is composed of two docker services (see docker-compose.yml):
        - patients-web: A web service running the Python FastAPI framework inside a Python 3.11 image.
        - patients-db: DB service running a MySql 5.7 database.

    The API has a main endpoint (POST /patients) to register new patients. It performs some basic validations, creates a record in the db and sends a notification to the patient using the notification service. An email channel has been configured to send notification emails, but in the near future any other channel can be easily configured.

    The second endpoint is a simple GET /patients to return all registered patients.

- Requirements:
    To build the images and run the app, you need to have Docker Desktop installed.

- To run the app:
    1. create an .env file with the required values and put it in the /app folder (see copy.env which has the required variables)
    2. run `docker-compose build'. This will build 2 images, one for the app and one for the mySQL DB.
    3. run `docker-compose up`. This will start the whole application. Wait at least 10 seconds for both services to initialise.
    4. The application is running!

- To run unit and e2e tests:
    1. Run both containers according to the `how to run app` guide.
    2. run `docker exec -it patients-web bash', this will init a bash console inside the app container
    3. run `python -m pytest` inside the container. This will run:
        1. e2e tests to test the endpoints
        2. unit tests for the notification service

- To manually test the API
    1. Run both containers following the `how to run app` guide
    2. Go to http://localhost:80/docs, Swagger will be displayed
    3. Run the endpoints manually

- Some good improvements that could be done to have a better API:
    * Improve tests

    * Currently the images are stored in the database. This can be improved by using an external service such as Amazon S3 or similar.

    * Add some kind of authentication (e.g. using bearer tokens)

    * Add a link to the registration email to confirm the registration using a new API endpoint. Allow only users who have confirmed their registration to use the application.

    * Add some linter (like flake8)

    * Format the code with a tool like Black