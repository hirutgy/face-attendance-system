# Face Attendance System

A face-recognition attendance app: detect a face, match it against registered users, and log check-ins. Built with **MTCNN** + **FaceNet512 (ONNX)**, **FastAPI**, **React + Vite**, and **SQLite**.

## Features

- Register users with **multiple photos** (1–5) for better accuracy
- **Recognize** a face or **mark attendance** in one step
- In-memory **embedding index** with batch cosine similarity search
- **Duplicate check-in prevention** (one attendance per user per day)
- Optional **admin API key** for registration
- **Rate limiting** on API endpoints
- Dashboard, analytics, and user profiles

## Architecture

```
Photo upload → MTCNN (face detect + align) → FaceNet ONNX (512-d embedding)
            → Cosine similarity match → SQLite (users, embeddings, attendance)
```

| Layer      | Stack                                      |
|------------|--------------------------------------------|
| Detection  | MTCNN (TensorFlow)                         |
| Embeddings | FaceNet512 ONNX via ONNX Runtime           |
| Backend    | FastAPI, SQLAlchemy, SQLite                |
| Frontend   | React 19, Vite, React Router               |
| Deploy     | Docker, Hugging Face Spaces, Vercel        |

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for frontend)
- **FaceNet model:** `models_local/facenet512.onnx` (not committed to git)

---

## Quick start

### Backend

```powershell
cd face-attendance-system
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python DOWNLOAD_FACENET.py
python -m backend.database.init_db

uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

- API: http://127.0.0.1:8000  
- Interactive docs: http://127.0.0.1:8000/docs  
- Health check: http://127.0.0.1:8000/health  

### Frontend

```powershell
cd frontend
npm install
copy .env.example .env
npm run dev
```

- App: http://localhost:5173  

---

## Testing the backend

### Automated tests (no server required)

```powershell
.\.venv\Scripts\Activate.ps1
pytest tests/ -v
```

Runs API smoke tests (`/health`, `/attendance/all`) and vector similarity unit tests.

### Manual tests (server must be running)

**Health**

```powershell
curl http://127.0.0.1:8000/health
```

Expected: `{"status":"ok","model_present":true}` — `model_present` is `false` if the ONNX file is missing.

**Register a user** (use a real face photo)

```powershell
curl -X POST "http://127.0.0.1:8000/register/register" `
  -F "name=Alice" `
  -F "files=@photo.jpg"
```

Multiple photos (recommended):

```powershell
curl -X POST "http://127.0.0.1:8000/register/register" `
  -F "name=Alice" `
  -F "files=@photo1.jpg" `
  -F "files=@photo2.jpg"
```

If `ADMIN_API_KEY` is set, add the header:

```powershell
curl -X POST "http://127.0.0.1:8000/register/register" `
  -H "X-Admin-Key: your-secret-key" `
  -F "name=Alice" `
  -F "files=@photo.jpg"
```

**Recognize**

```powershell
curl -X POST "http://127.0.0.1:8000/recognize/" `
  -F "file=@photo.jpg"
```

**Mark attendance**

```powershell
curl -X POST "http://127.0.0.1:8000/attendance/" `
  -F "file=@photo.jpg"
```

**List attendance**

```powershell
curl http://127.0.0.1:8000/attendance/all
curl http://127.0.0.1:8000/attendance/today
```

**Analytics & profile**

```powershell
curl http://127.0.0.1:8000/attendance/analytics/
curl http://127.0.0.1:8000/users/profile/1
```

The easiest way to try all endpoints is the **Swagger UI** at http://127.0.0.1:8000/docs.

---

## API reference

| Method | Endpoint                    | Description                          |
|--------|-----------------------------|--------------------------------------|
| GET    | `/health`                   | Server + model status                |
| POST   | `/register/register`        | Register user (multi-photo)          |
| POST   | `/recognize/`               | Identify face (`?log=true` to log)   |
| POST   | `/attendance/`              | Recognize + log attendance           |
| GET    | `/attendance/all`           | All attendance records               |
| GET    | `/attendance/today`         | Today's check-ins                    |
| GET    | `/attendance/analytics/`    | Stats (totals, per person/day)       |
| GET    | `/users/profile/{user_id}`  | User profile + recent check-ins      |
| POST   | `/detect/`                  | Face detection only                  |
| POST   | `/embed/`                   | Generate embedding from face photo   |

**Upload fields**

- Register: `name` (form) + `files` (one or more images)
- Recognize / attendance / detect / embed: `file` (single image)

**Supported image types:** JPG, JPEG, PNG, WebP, GIF, BMP, TIFF (max 5 MB by default)

---

## Environment variables

Copy `.env.example` and adjust as needed.

### Backend

| Variable           | Default   | Description                                      |
|--------------------|-----------|--------------------------------------------------|
| `ADMIN_API_KEY`    | (empty)   | If set, registration requires `X-Admin-Key`      |
| `MATCH_THRESHOLD`  | `0.7`     | Cosine similarity threshold for a match          |
| `MAX_UPLOAD_BYTES` | `5242880` | Max upload size (5 MB)                           |
| `CORS_ORIGINS`     | `*`       | Comma-separated allowed origins                  |
| `RATE_LIMIT`       | `30/minute` | Global API rate limit                          |
| `DATABASE_URL`     | SQLite path | Override database connection                 |

### Frontend (`frontend/.env`)

| Variable              | Default                  | Description                |
|-----------------------|--------------------------|----------------------------|
| `VITE_API_BASE`       | `http://127.0.0.1:8000`  | Backend URL                |
| `VITE_ADMIN_API_KEY`  | (empty)                  | Sent on register requests  |

---

## Docker

Run **both backend and frontend** with Docker Compose:

```powershell
# From project root — place facenet512.onnx in models_local/ first
docker compose up --build
```

| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |
| API docs | http://localhost:8000/docs |

Stop containers:

```powershell
docker compose down
```

### Environment (optional)

Create a `.env` file in the project root:

```env
ADMIN_API_KEY=your-secret-key
VITE_API_BASE=http://localhost:8000
MATCH_THRESHOLD=0.7
```

`VITE_API_BASE` must be a URL your **browser** can reach (usually `http://localhost:8000`, not the internal Docker service name).

### Volumes

- `./models_local` — FaceNet ONNX model (mounted into backend)
- `attendance_data` — SQLite database (persists between restarts)

### Backend only

```powershell
docker compose up --build backend
```

### Frontend only (requires backend running)

```powershell
docker compose up --build frontend
```

### Build individual images

```powershell
docker build -f backend/Dockerfile -t face-attendance-backend .
docker build -f frontend/Dockerfile -t face-attendance-frontend ./frontend
```

---

## Deploy backend on Hugging Face Spaces

Hugging Face Spaces (Docker) hosts the FastAPI backend. The frontend on Vercel will call this API URL.

### 1. Prepare the model

Place `facenet512.onnx` in `models_local/` locally, or plan to upload it to the Space after creation.

### 2. Create a Docker Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **Docker** as the SDK
3. Pick **CPU basic** (or higher if you need more RAM for TensorFlow/MTCNN)
4. Create the Space

### 3. Push backend code to the Space

**Option A — connect this GitHub repo**

1. In Space **Settings → Repository**, connect your GitHub repo
2. Set the Dockerfile path to `deploy/huggingface/Dockerfile` if your Space settings allow it, **or** copy that file to `Dockerfile` at the repo root for the Space

**Option B — push files manually**

Upload these paths from this project into the Space repo:

```
requirements.txt
backend/
DOWNLOAD_FACENET.py
models_local/facenet512.onnx
Dockerfile          ← use deploy/huggingface/Dockerfile
README.md           ← use deploy/huggingface/README.md (includes Space frontmatter)
```

### 4. Configure Space environment variables

In the Space → **Settings → Variables and secrets**:

| Variable | Value |
|----------|--------|
| `ADMIN_API_KEY` | A strong secret for registration |
| `CORS_ORIGINS` | Your Vercel URL, e.g. `https://face-attendance.vercel.app` |
| `MATCH_THRESHOLD` | `0.7` (optional) |

### 5. Build and verify

After the Space builds, your API base URL is:

```
https://<your-username>-<space-name>.hf.space
```

Test it:

```bash
curl https://<your-username>-<space-name>.hf.space/health
```

Open API docs:

```
https://<your-username>-<space-name>.hf.space/docs
```

### Hugging Face notes

- The Docker image listens on port **7860** (required by Hugging Face Spaces).
- SQLite data on free Spaces may **reset** when the Space restarts or rebuilds.
- First request can be slow while MTCNN and FaceNet load.
- Increase Space hardware if you hit memory limits (TensorFlow + ONNX).

---

## Deploy frontend on Vercel

Vercel hosts the static React build. It talks to your Hugging Face backend via `VITE_API_BASE`.

### 1. Import the project

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure the project:

| Setting | Value |
|---------|--------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### 2. Set environment variables

In Vercel → **Project → Settings → Environment Variables**:

| Name | Value | Example |
|------|--------|---------|
| `VITE_API_BASE` | Your Hugging Face Space URL | `https://your-username-face-attendance-api.hf.space` |
| `VITE_ADMIN_API_KEY` | Same as backend `ADMIN_API_KEY` | `your-secret-key` |

Apply to **Production**, **Preview**, and **Development**.

> `VITE_*` variables are baked in at **build time**. Redeploy after changing them.

### 3. Deploy

Click **Deploy**. Vercel will build and host the app at:

```
https://<your-project>.vercel.app
```

`frontend/vercel.json` is included for React Router (all routes serve `index.html`).

### 4. Update backend CORS

After you know the Vercel URL, set this on the Hugging Face Space:

```
CORS_ORIGINS=https://<your-project>.vercel.app
```

Redeploy or restart the Space if needed.

### 5. End-to-end test

1. Open your Vercel URL
2. **Register** a user with a face photo
3. **Recognize** / **Check In** with the same person
4. Open **Dashboard** to confirm attendance

---

## Deployment checklist

| Step | Backend (Hugging Face) | Frontend (Vercel) |
|------|------------------------|-------------------|
| 1 | Create Docker Space | Import repo, root = `frontend` |
| 2 | Add `facenet512.onnx` to `models_local/` | Set `VITE_API_BASE` to HF Space URL |
| 3 | Set `ADMIN_API_KEY` | Set `VITE_ADMIN_API_KEY` (same key) |
| 4 | Set `CORS_ORIGINS` to Vercel URL | Deploy |
| 5 | Verify `/health` and `/docs` | Test register → recognize → dashboard |

---

## Project structure

```
face-attendance-system/
├── backend/
│   ├── api/              # FastAPI route handlers
│   ├── attendance/       # Analytics helpers
│   ├── database/         # SQLAlchemy models, CRUD, SQLite
│   ├── detection/        # MTCNN face detection
│   ├── models/           # FaceNet ONNX inference
│   ├── recognition/      # Embedding index + matching engine
│   ├── config.py         # Environment settings
│   └── main.py           # App entry point
├── frontend/             # React UI
├── models_local/         # facenet512.onnx (gitignored)
├── tests/                # pytest suite
├── DOWNLOAD_FACENET.py   # Model download helper
├── backend/Dockerfile    # Backend image
├── frontend/Dockerfile   # Frontend image (nginx)
├── deploy/
│   └── huggingface/      # HF Spaces Dockerfile + Space README template
├── docker-compose.yml    # Run both services locally
├── requirements.txt
└── evaluation_report.txt # Offline benchmark results
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'tensorflow'` | Run `pip install -r requirements.txt` |
| `FaceNet model not found` | Run `python DOWNLOAD_FACENET.py` or place `facenet512.onnx` in `models_local/` |
| `No face detected` | Use a clear, front-facing photo (JPEG/PNG/WebP) |
| `Invalid or missing admin API key` | Set `X-Admin-Key` header or clear `ADMIN_API_KEY` for dev |
| `Already checked in today` | Expected — duplicate prevention is working |
| Frontend can't reach API | Check `VITE_API_BASE` and that uvicorn is on port 8000 |
| CORS error on Vercel | Set `CORS_ORIGINS` on Hugging Face to your exact Vercel URL (`https://...`) |
| HF Space build fails | Ensure `Dockerfile` uses port **7860** (`deploy/huggingface/Dockerfile`) |
| HF `/health` shows `model_present: false` | Upload `facenet512.onnx` to `models_local/` in the Space |
| Vercel shows old API URL | Redeploy after changing `VITE_*` env vars (build-time) |
| Slow first request | Normal — MTCNN and FaceNet load lazily on first use |

---

## Evaluation

Offline benchmark results are in [`evaluation_report.txt`](evaluation_report.txt):

- **Accuracy:** ~90%
- **Macro F1:** ~0.87

---

## License

Add your license here.
