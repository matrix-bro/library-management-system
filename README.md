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

1. User APIs

### Create a New User

Endpoint: `POST /api/register/`

### List All Users (excluding admin)

Endpoint: `GET /api/users/`

### Get User by ID

Endpoint: `GET /api/users/{user_id}/`

2. Book APIs

### Add a New Book

Endpoint: `POST /api/books/create/`
Permissions: Requires authentication

### List All Books

Endpoint: `GET /api/books/list/`

### Get Book by ID

Endpoint: `GET /api/books/details/{book_id}/`

### Assign/Update Book Details

Endpoint: `PUT /api/books/update/{book_id}/`

3. BorrowedBooks APIs

### Borrow a Book

Endpoint: `POST /api/books/borrow/{user_id}/{book_id}/`

### Return a Book

Endpoint: `PUT /api/books/return/{book_id}/`

### List All Borrowed Books

Endpoint: `GET /api/books/currently_borrowed/`

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
