# Homework

## Frameworks used

* **Flask** - Flask was chosen due to its suitable for a smaller web app project like this.
* **PyTest** - PyTest is used as the test framework. This allows us to easily create the test fixtures that are needed.
* **MongoDB** - MongoDB allows us to easily create a composite text index, making it a good choice for the requirements of this project.

## Security

The instructions below assume this app is being used for testing. A production implementation would have to securely store the MongoDB connection string and the secret key. This would be passed in to the app as environment variables using `MONGO_URI` and `SECRET_KEY`, respectively.

## How to Run

Note: The instructions below were tested on Windows 11. Actual commands to run may vary slightly on Linux.

### Start the Database Server

1. Run

    ```ps1
    docker run --name mongo -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password -d -p 27017:27017 mongo:6.0.5
    ```

2. Create a new virtual environment:

    ```ps1
    python -m venv venv
    ```

3. Activate the virtual environment:

    ```ps1
    .\venv\Scripts\activate
    ```

4. If using VSCode, set your current Python interpreter to the newly created venv.

5. From the project root, install the dependencies:

    ```ps1
    pip install -r requirements.txt
    ```

6. Run the app:

    ```ps1
    flask run project/__init__.py
    ```

The web service will be available at: <http://localhost:5000/>

## Run Unit Tests

Since the majority of the logic is in the MongoDB queries, the unit tests have been implemented as functional tests against an instance of MongoDB. With more time, this could be enhanced to use a mocking instance, such as [MongoMock](https://github.com/mongomock/mongomock).

First, follow the steps for running the app, including starting the MongoDB Docker container and installing the requirements.

Run pytest:

```ps1
python -m pytest tests/
```

Or run pytest and generate a coverage report:

```ps1
python -m pytest --cov-report term-missing --cov=project tests/
```

## Tools Used

* VSCode for development.
* Black for code formatting.
* isort for organizing inputs.

## Searching

A composite index has been created so that you can search both the title and content of the notes. Multiple search terms can be used with a space as the delimiter. In the query string, this is escaped with `%20`. For example, `http://localhost:5000/api/search?q=first%20second`

## Rate-Limiting

Rate limiting is implemented with [Flask-Limiter](https://flask-limiter.readthedocs.io/en/stable/) and is set to a maximum of 200 requests per day and 50 requests per hour. These values could be further configured on each API function. However, these were left as the default values for the purpose of this excercise.

## Authentication

A JWT is returned from the `/api/auth/login` call. For the calls requiring authentication, this token must be passed in a header called `x-access-tokens`.

## Postman

A Postman collection called `postman_collection.json` can be found in the root of this repo. Be sure to replace the `x-access-tokens` with a valid token before running any of the authenticated calls.
