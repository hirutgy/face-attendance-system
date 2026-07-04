---
title: Face Attendance API
emoji: 🧑
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# Face Attendance API

FastAPI backend for the Face Attendance System.

## Health check

`GET /health`

## API docs

`/docs`

## Environment variables (Space settings → Variables)

| Variable | Example |
|----------|---------|
| `ADMIN_API_KEY` | your-secret-key |
| `CORS_ORIGINS` | `https://your-app.vercel.app` |
| `MATCH_THRESHOLD` | `0.7` |

## Model file

Upload `facenet512.onnx` to `models_local/` in this Space, or add it before building the Docker image.
