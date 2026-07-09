const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
console.log("API_BASE =", API_BASE);
const ADMIN_KEY = import.meta.env.VITE_ADMIN_API_KEY || "";

const adminHeaders = () =>
    ADMIN_KEY ? { "X-Admin-Key": ADMIN_KEY } : {};

export const registerUser = async (formData) => {
    const response = await fetch(`${API_BASE}/register/register`, {
        method: "POST",
        headers: adminHeaders(),
        body: formData,
    });
    return response.json();
};
export const fetchUsers = async () => {
    const response = await fetch(`${API_BASE}/users/`);
    return response.json();
};

export const recognizeUser = async (formData, logAttendance = false) => {
    const url = new URL(`${API_BASE}/recognize/`);
    if (logAttendance) {
        url.searchParams.set("log", "true");
    }
    const response = await fetch(url, {
        method: "POST",
        body: formData,
    });
    return response.json();
};

export const markAttendance = async (formData) => {
    const response = await fetch(`${API_BASE}/attendance/`, {
        method: "POST",
        body: formData,
    });
    return response.json();
};

export const fetchAttendance = async () => {
    const response = await fetch(`${API_BASE}/attendance/all`);
    return response.json();
};

export const fetchAnalytics = async () => {
    const response = await fetch(`${API_BASE}/attendance/analytics/`);
    return response.json();
};

export const fetchUserProfile = async (userId) => {
    const response = await fetch(`${API_BASE}/users/profile/${userId}`);
    if (!response.ok) {
        return null;
    }
    return response.json();
};

export { API_BASE };
export const chatWithAssistant = async (message) => {
    const response = await fetch(`${API_BASE}/assistant/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message }),
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Assistant request failed.");
    }

    return data;
};