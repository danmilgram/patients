# Patient registration system

- Requirements:
    In order to build the images and run the app this requires docker desktop installed.

- How to run app:
    1. create a .env file with the required values and put it in the /app folder (see copy.env which has the required variables)
    2. run `docker-compose build` . This builds 2 images, one for the app and one for the mySQL DB
    3. run `docker-compose up`. This will start the whole application. Wait for at least 10 seconds to get both services initialized.
    4. App is running!

- How to run unit and e2e tests:
    1. Run both containers following `how to run app` guide
    2. run ` docker exec -it [containername] bash`, this will init a bash console inside the app container (replace [containername] with your web container name)
    3. inside the container run `python -m pytest`. This will run:
        1. e2e tests to test the endpoints
        2. unit tests for the notifications service

- How to manually test the API
    1. Run both containers following `how to run app` guide
    2. Go to http://localhost:80/docs , Swagger will be show
    3. Manually execute the endpoints

- Some good improvements that could be done in order to have a better API:
    * Add some linter
    * Improve tests
    * Add some kind of athentication (for example using bearer tokens)
    * Currently the images are saved in the database. That solution can be improved using an external service like Amazon S3 or similar.
