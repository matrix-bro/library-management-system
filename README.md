# Library Management System

A library management system created using Django

## Project Setup

1. Clone the repository:

```bash
git clone https://github.com/matrix-bro/library-management-system.git
```

2. Go to project's folder

```bash
cd library-management-system
```

3. Create a virtual environment and activate it

```bash
python -m venv venv

(In windows)
source .\venv\Scripts\activate

(In linux)
source venv/bin/activate
```

4. Install from requirements file

```bash
pip install -r requirements.txt
```

5. Setup PostgreSQL and Environment Variables

- Create a database
- Copy `example.env` file and rename it to `.env`
- Change `database name, user, password and secret key`

6. Apply migrations

```bash
python manage.py migrate
```

7. Start the development server

```bash
python manage.py runserver
```

## API Documentation

> Note: All the APIs require authentication except `Create a New User API`

- To include authentication tokens in your requests
  - First, create an account using `Create a New User API` mentioned below
  - Login Endpoint: `POST /api/token/`
    - Login using email and password
    - Copy the access token
  - Now, in the `Authorization Header`, choose `Bearer Token` and paste the `access token` there

## 1. User APIs

### Create a New User

Endpoint: `POST /api/register/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
- Body:

```json
{
  "name": "John Doe",
  "email": "john@gmail.com",
  "membership_date": "2024-01-30",
  "password": "password",
  "password2": "password"
}
```

- Response:

```json
{
  "success": "User account created successfully.",
  "data": {
    "name": "John Doe",
    "email": "john@gmail.com",
    "membership_date": "2024-01-30"
  },
  "status": 201
}
```

### List All Users (excluding admin)

Endpoint: `GET /api/users/`

Request:

- Method: `GET`
- Headers:

  - `Authorization: Bearer {your_access_token}`

- Response:

```json
[
  {
    "user_id": 1,
    "name": "John Doe",
    "email": "john@gmail.com",
    "membership_date": "2024-01-30"
  },
  {
    "user_id": 2,
    "name": "Another User",
    "email": "another@gmail.com",
    "membership_date": "2024-01-31"
  }
]
```

### Get User by ID

Endpoint: `GET /api/users/{user_id}/`

Request:

- Method: `GET`
- Headers:

  - `Authorization: Bearer {your_access_token}`

- Response:

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@gmail.com",
  "membership_date": "2024-01-30"
}
```

## 2. Book APIs

### Add a New Book

Endpoint: `POST /api/books/create/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`
- Body:

```json
{
  "title": "Book 1",
  "isbn": "123456789",
  "published_date": "2023-01-01",
  "genre": "genre1"
}
```

- Response:

```json
{
  "title": "Book 1",
  "isbn": "123456789",
  "published_date": "2023-01-01",
  "genre": "genre1"
}
```

### List All Books

Endpoint: `GET /api/books/list/`

Request:

- Method: `GET`
- Headers:

  - `Authorization: Bearer {your_access_token}`

- Response:

```json
[
  {
    "title": "Book 2",
    "isbn": "456123789",
    "published_date": "2022-01-01",
    "genre": "genre2"
  },
  {
    "title": "Book 1",
    "isbn": "123456789",
    "published_date": "2023-01-01",
    "genre": "genre1"
  }
]
```

### Get Book by ID

Endpoint: `GET /api/books/details/{book_id}/`

Request:

- Method: `GET`
- Headers:

  - `Authorization: Bearer {your_access_token}`

- Response:

```json
{
  "title": "Book 2",
  "isbn": "456123789",
  "published_date": "2022-01-01",
  "genre": "genre2"
}
```

### Assign/Update Book Details

Endpoint: `PUT /api/books/update/{book_id}/`

Request:

- Method: `PUT`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`
- Body:

```json
{
  "title": "Book 1 updated",
  "isbn": "10112345",
  "published_date": "2023-01-30",
  "genre": "genre 1 updated",
  "book_details": {
    "number_of_pages": 100,
    "publisher": "publisher 1",
    "language": "en"
  }
}
```

- Response:

```json
{
  "message": "Book details updated successfully.",
  "data": {
    "title": "Book 1 updated",
    "isbn": "10112345",
    "published_date": "2023-01-30",
    "genre": "genre 1 updated",
    "book_details": {
      "number_of_pages": 100,
      "publisher": "publisher 1",
      "language": "en"
    }
  },
  "code": 200
}
```

## 3. BorrowedBooks APIs

### Borrow a Book

Endpoint: `POST /api/books/borrow/{user_id}/{book_id}/`

Request:

- Method: `POST`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`
- Body:

```json
{
  "borrow_date": "2024-01-30"
}
```

- Response:

```json
{
  "message": "Book borrowed successfully.",
  "code": 200
}
```

### Return a Book

Endpoint: `PUT /api/books/return/{book_id}/`

Request:

- Method: `PUT`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: Bearer {your_access_token}`
- Body:

```json
{
  "return_date": "2024-01-31"
}
```

- Response:

```json
{
  "message": "Book returned successfully.",
  "code": 200
}
```

### List All Borrowed Books

Endpoint: `GET /api/books/currently_borrowed/`

Request:

- Method: `GET`
- Headers:

  - `Authorization: Bearer {your_access_token}`

- Response:

```json
{
  "message": "List of currently borrowed books",
  "data": [
    {
      "id": 2,
      "borrow_date": "2024-01-30",
      "return_date": null,
      "user": 2,
      "book": 2
    },
    {
      "id": 1,
      "borrow_date": "2024-01-30",
      "return_date": null,
      "user": 1,
      "book": 1
    }
  ],
  "code": 200
}
```

## Running Tests

To run all tests, use the following command:

```bash
python manage.py test
```

To run user tests,

```bash
python manage.py test app.test_user
```

To run book tests,

```bash
python manage.py test app.test_book
```
