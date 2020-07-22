# Bookshelf App

This app allows users to display books as part of their library. Users can add new books to their library with title, author and rating; update their rating of existing entries; or delete existing entries. This app uses python3, nodejs, and a postgresql database.

## Set-up

### Backend

Navigate to the backend folder

Set-up a virtual environment and activate it:

```bash
python3 -m venv env
source env/bin/activate
```

You should see (env) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

Install the requirements:

```bash
pip install -U pip
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo FLASK_APP=flaskr >> .env
```

Initialize and set up the database:

```bash
dropdb bookshelf
createdb bookshelf
psql bookshelf < books.psql
```

### Frontend

Navigate to the frontend folder

Install the requirements:

```bash
npm install
```

## Usage

To start the backend, navigate to the backend folder and make sure you are in the virtual environment (you should see (env) before your command prompt). If not `source /env/bin/activate` to enter it.

```bash
Usage: flask run
```

To start the frontend, run the following command in another terminal from the frontend folder:

```bash
Usage: npm start
```

Navigate to `http://127.0.0.1:3000/` to see the app in action!

## Screenshots

![Bookshelf App Homepage](https://i.imgur.com/JM5BbJP.png)

## API Reference

### Base URL

When running locally with the built in flask server, the base URL is as follows:

```bash
http://127.0.0.1:5000/
```

### Error Handling

Below are a list of errors that may be raised as part of the API

#### 400: Bad Request

This is returned when the request is malformed in some way. (i.e. Required info is missing)

#### 404: Not Found

This is returned when the requested resource does not exist. (i.e. Attempting to view a page of books that don't exist)

#### 405: Method Not Allowed

This is returned when the incorrect request method is specified at an endpoint. (i.e. Attempting to delete without specifying a specific book to delete)

#### 422: Unprocessable Entity

This is returned when the request is unable to be fulfilled in some way. (i.e. Attempting to update a book that has previously been deleted)

#### 500: Internal Server Error

This is returned when something there is a problem with the server.

### Endpoints

Books:

#### GET /books

Retrieve a list of paginated books

Example Request:

```bash
curl http://127.0.0.1:5000/books?page=1
```

Parameters:

- page (int) [optional]: Each page returns the next 8 results (default: 1)

Example Response:

```bash
{
  "success": true,
  "books": [
    {
      "id": 1,
      "title": "Anansi Boys",
      "author": "Neil Gaiman",
      "rating": 5
    }
  ],
  "total_books": 1
}
```

#### POST /books

Create a new book or search all books

##### New Book

Example Request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"title": "Nevermore", "author": "Neil Gaiman", "rating": "5"}' http://127.0.0.1:5000/books
```

Parameters:

- title (str): Title of the new book
- author (str): Author of the new book
- rating (int) [optional]: Rating of the new book

Example Response:

```bash
{
  "success": true,
  "created_book_id": 2,
  "books": [
    {
      "id": 1,
      "title": "Anansi Boys",
      "author": "Neil Gaiman",
      "rating": 5
    },
    {
      "id": 2,
      "title": "Nevermore",
      "author": "Neil Gaiman",
      "rating": 5
    }
  ],
  "total_books": 2
}
```

##### Search Books

Example Request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"search": "Anansi Boys"}' http://127.0.0.1:5000/books
```

Parameters:

- search (str): The string to search for in the bookshelf

Example Response:

```bash
{
  "success": true,
  "books": [
    {
      "id": 1,
      "title": "Anansi Boys",
      "author": "Neil Gaiman",
      "rating": 5
    }
  ],
  "total_books": 1
}
```

#### PATCH /books/<book_id>

Update a book's rating

Example Request:

```bash
curl -X PATCH -H "Content-Type: application/json" -d '{"rating": "4"}' http://127.0.0.1:5000/books/1
```

Parameters:

- rating (int): The rating to update the book to

Example Response:

```bash
{
    "success": true,
    "updated_book_id": 1,
    "old_rating": 5,
    "new_rating": 4
}
```

#### DELETE /books/<book_id>

Delete a book

Example Request:

```bash
curl -X DELETE http://127.0.0.1:5000/books/1
```

Example Response:

```bash
{
  "success": true,
  "deleted_book_id": 1,
  "books": [
    {
      "id": 2,
      "title": "Nevermore",
      "author": "Neil Gaiman",
      "rating": 5
    }
  ],
  "total_books": 1
}
```

## Testing Suite

The backend has a testing suite to test all of the API endpoints

To set up the test database:

```bash
cd backend
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
```

To run all the tests:

```bash
Usage: test_flaskr.py
```

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Bookshelf App is licensed under the [MIT license](https://github.com/danrneal/bookshelf-app/blob/master/LICENSE).
