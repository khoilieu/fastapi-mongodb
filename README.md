# FastAPI Project

This project is a FastAPI application that provides a platform for user management and forum posts. It utilizes MongoDB for data storage and includes user authentication features.

## Project Structure

```
fast_api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   └── .env
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd fast_api
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the `app` directory and add your MongoDB URI:
   ```
   MONGO_URI=mongodb://localhost:27017
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

## Docker Instructions

To build and run the application using Docker, follow these steps:

1. **Build the Docker image:**
   ```bash
   docker build -t fastapi-app .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -d -p 80:80 fastapi-app
   ```

## API Endpoints

- **User Management:**
  - `POST /users/`: Create a new user.
  - `GET /users/{id}`: Retrieve a user by ID.
  - `PATCH /users/{id}`: Update a user by ID.
  - `DELETE /users/{id}`: Delete a user by ID.

- **Authentication:**
  - `POST /token`: Obtain a JWT token for authentication.

- **Forum Posts:**
  - `POST /posts/`: Create a new forum post.
  - `GET /posts/{id}`: Retrieve a forum post by ID.
  - `PATCH /posts/{id}`: Update a forum post by ID.
  - `DELETE /posts/{id}`: Delete a forum post by ID.

## License

This project is licensed under the MIT License.