# Bookshelf App

This app allows users to display books as part of their library. Users can add new books to thier library with title, author and rating; update their rating of existing entries; or delete existing entries. This app uses python3, nodejs, and a postgresql database.

## Set-up

Set-up a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see (venv) before your command prompt now. (You can type `deactivate` to exit the virtual environment any time.)

### Backend

Navigate to the backend folder

Install the requirements:

```bash
pip install -r requirements.txt
```

Set up your environment variables:

```bash
touch .env
echo FLASK_APP=flaskr >> .env
echo FLASK_ENV=development >> .env
```

### Frontend

Navigate to the frontend folder

Install the requirements:

```bash
npm install
```

## Usage

To start the backend, run the following command from the backend folder:

```bash
flask run
```

To start the frontend, run the following command in another terminal from the frontend folder:

```bash
npm start
```

Navigate to `http://127.0.0.1:3000/` to see the app in action!

## Screenshots

![Bookshelf App Homepage](https://i.imgur.com/FDRRRV6.png)

## API Reference

### Base URL

When running locally with the built in flask server, the base url is as follows:

```bash
http://127.0.0.1:5000/
```

### Error Handling

Below are a list of errors that may be raised as part of the api

#### 400: Bad Reqeuest

This is returned when the requested is malformed in some way. (i.e. Required info is missing)

#### 404: Not Found

This is returned when the requested resource does not exist. (i.e. Attempting to view a page of books that don't exist)

#### 405: Method Not Allowed

This is returned when the incorrect request method is specified at an endpoint (i.e. Attempting to delete with specifying a specific book to delete)

#### 422: Unprocessable Entity

This is returned when the request is to be fuffilled in some way (i.e. Attempting to update a book that has previously been deleted)

### Endpoints

Books:

#### GET /books

```bash
curl http://127.0.0.1:5000/books?page=1
```

* page [int] (optional): Each page returns the next 8 results (default: 1)

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

##### New Book

```bash
curl -X POST Content-Type: application/json -d {"title": "Nevermore", "author": "Neil Gaiman", "rating": "5"} http://127.0.0.1:5000/books
```

* title [str]: Title of the new book
* author [str]: Author of the new book
* rating [int] (optional): Rating of the new book

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

##### Sample Request (Search)

```bash
curl -X POST Content-Type: application/json -d {"search": "Anansi Boys"} http://127.0.0.1:5000/books?page=1
```

##### Arguments (Search)

page [int] (optional): Each page returns the next 8 results (default: 1)
search [str]: The string to search for in the bookshelf

##### Sample Response (Search)

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

```bash
curl -X PATCH Content-Type: application/json -d {"rating": "4"} http://127.0.0.1:5000/books/1
```

* rating [int]: The rating to update the book to

```bash
{
    "success": true,
    "updated_book_id": 1
}
```

#### DELETE /books/<book_id>

```bash
curl -X DELETE http://127.0.0.1:5000/books/1
```

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
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
```

To run all the tests:

```bash
usage: ./backend/test_flaskr.py
```

## Credit

[Udacity's Full Stack Web Developer Nanodegree Program](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044)

## License

Fyyur is licensed under the [MIT license](https://github.com/danrneal/bookshelf-app/blob/master/LICENSE).
