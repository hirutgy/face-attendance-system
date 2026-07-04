export const API_BASE = "http://127.0.0.1:8000";

// REGISTER USER
export async function registerUser(name, file) {
    const formData = new FormData();
    formData.append("name", name);
    formData.append("image", file);   // MUST match FastAPI parameter

    const response = await fetch(`${API_BASE}/register`, {
        method: "POST",
        body: formData
    });

    return response.json();
}

// RECOGNIZE USER
export async function recognizeUser(file) {
    const formData = new FormData();
    formData.append("image", file);

    const response = await fetch(`${API_BASE}/recognize`, {
        method: "POST",
        body: formData
    });

    return response.json();
}
