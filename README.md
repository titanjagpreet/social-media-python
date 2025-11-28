# 📸 Simple Social — Full-Stack Social Media App

A minimal **full-stack social media platform** built using:

* **FastAPI** — Backend API
* **FastAPI Users** — Authentication (JWT)
* **SQLAlchemy Async ORM** — Database Models
* **SQLite (aiosqlite)** — Local database
* **ImageKit** — Media upload & transformations
* **Streamlit** — Frontend UI

Users can **register, log in, upload posts, view a feed, and delete their own posts**.

---

# 🚀 Features

### 🔐 Authentication

* Register
* Login (JWT tokens)
* Protected routes
* `/auth/users/me` profile endpoint

### 📤 Media Upload

* Upload **images or videos**
* Files stored using **ImageKit CDN**
* Temporary-file safe upload handling (Windows-friendly)
* Automatic detection of file types

### 📰 Feed

* Displays newest posts first
* Shows:

  * Caption
  * Media
  * User email
  * Timestamp
  * Owner badge
* Supports overlay text using ImageKit transformation
* Auto-resizes images/videos

### 🗑️ Delete Post

* Only the **owner** of the post can delete it
* Ownership verified via JWT user ID

### 🖥️ Streamlit Frontend

* Login & Signup
* Upload UI
* Dynamic feed
* Safe error handling
* Nice clean UI

---

# 🧱 Tech Stack

| Layer             | Technology                |
| ----------------- | ------------------------- |
| **Backend**       | FastAPI                   |
| **Auth**          | FastAPI Users (JWT)       |
| **DB**            | SQLite + Async SQLAlchemy |
| **ORM Models**    | DeclarativeBase           |
| **Media Storage** | ImageKit                  |
| **Frontend**      | Streamlit                 |
| **Language**      | Python 3.11+              |

---

# 📂 Project Structure

```
project/
│
├── app/
│   ├── app.py               # FastAPI application + routes
│   ├── db.py                # Database models + session
│   ├── users.py             # Auth manager + FastAPI Users setup
│   ├── schemas.py           # Pydantic schemas
│   ├── images.py            # ImageKit initialization
│
├── streamlit_frontend.py    # Streamlit UI
├── test.db                  # SQLite database (ignored via .gitignore)
├── .env                     # ImageKit keys + secrets
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup Instructions

## 1️⃣ Create Virtual Environment & Install Dependencies

```bash
uv venv fastapi-env
source fastapi-env/bin/activate

pip install -r requirements.txt
```

Minimal dependencies:

```
fastapi
uvicorn
sqlalchemy
aiosqlite
imagekitio
python-multipart
fastapi-users[sqlalchemy]
streamlit
python-dotenv
```

---

# 🔑 2️⃣ Environment Variables (`.env`)

Create a `.env` file:

```
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL=https://ik.imagekit.io/your_id
JWT_SECRET=titanxbt
```

---

# 🗄️ 3️⃣ Run the Backend

```bash
uv run app/app.py
```

API will start on:

```
http://localhost:8000
```

Docs:

```
http://localhost:8000/docs
```

---

# 🖥️ 4️⃣ Run the Streamlit Frontend

```bash
streamlit run streamlit_frontend.py
```

Runs on:

```
http://localhost:8501
```

---

# 🧩 API Overview

### 🔐 AUTH ROUTES (FastAPI Users)

| Method | Route             | Description                 |
| ------ | ----------------- | --------------------------- |
| POST   | `/auth/register`  | Create new user             |
| POST   | `/auth/jwt/login` | Login, get JWT access token |
| GET    | `/auth/users/me`  | Get logged-in user          |

---

### 📤 POST /upload

Upload image or video + caption.

Request (multipart form):

```
file: <binary>
caption: <string>
```

Response:

```json
{
  "id": "uuid",
  "caption": "hello",
  "url": "https://ik.imagekit.../file.jpg",
  "file_type": "image",
  "file_name": "abc123",
  "created_at": "2025-11-25T10:41:00"
}
```

---

### 📰 GET /feed

Returns an array of posts:

```json
[
  {
    "id": "...",
    "user_id": "...",
    "caption": "...",
    "url": "...",
    "file_type": "image",
    "file_name": "...",
    "created_at": "...",
    "is_owner": true,
    "email": "user@example.com"
  }
]
```

---

### 🗑️ DELETE /posts/{post_id}

Only the **owner** can delete:

```json
{"success": true, "message": "Post deleted successfully"}
```

---

# 🎨 UI Overview (Streamlit)

### Login Page

* Email + password
* Login button
* Signup button

### Upload Page

* Upload file
* Add caption
* Share button

### Feed Page

* Shows posts
* Shows caption overlays
* Shows user email
* Shows delete button if owner

---

# 🧪 Local Media Testing

To show a local file through Streamlit, the project already includes handling for:

```
/mnt/data/6547e46f-66dd-4e2a-847a-15b99f66cf32.png
```

This is used automatically if the backend returns no URL.

---

# 🔥 Future Improvements

* Pagination for feed
* Like & comment system
* Follow/unfollow system
* Real-time notifications
* Local storage for videos during testing
* Docker containerization

---

# ❤️ Credits

Built with:

* FastAPI
* Streamlit
* ImageKit
* SQLAlchemy
* FastAPI Users
