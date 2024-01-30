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
