import "./Register.css";
import { useState } from "react";
import { registerUser } from "../api/api";
import FileUpload from "../components/FileUpload/FileUpload";
import PageHeader from "../components/PageHeader/PageHeader";

export default function Register() {
    const [name, setName] = useState("");
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const resetForm = () => {
        setName("");
        setImages([]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!name.trim()) {
            setMessage("Please enter a full name.");
            return;
        }

        if (images.length === 0) {
            setMessage("Please upload at least one face image.");
            return;
        }

        setLoading(true);
        setMessage("");

        try {
            const formData = new FormData();

            formData.append("name", name);

            images.forEach((image) => {
                formData.append("files", image);
            });

            const result = await registerUser(formData);

            if (result.status === "success") {
                setMessage(`✅ ${result.message}`);
                resetForm();
            } else {
                setMessage(
                    result.message ||
                    result.detail ||
                    "Registration failed."
                );
            }
        } catch (error) {
            setMessage(error.message || "Unable to connect to the server.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <PageHeader
                icon="👤"
                title="Register New User"
                subtitle="Register a new person by entering their name and uploading between 1 and 5 clear face images."
            />

            <form className="form" onSubmit={handleSubmit}>
                <div className="form-card">
                    <div className="form-section">
                        <h3>Student Information</h3>

                        <label className="form-label">
                            Full Name

                            <input
                                type="text"
                                placeholder="Enter student's full name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                disabled={loading}
                                required
                            />
                        </label>
                    </div>

                    <div className="form-section">
                        <h3>Face Images</h3>

                        <FileUpload
                            multiple
                            maxFiles={5}
                            files={images}
                            onChange={setImages}
                            disabled={loading}
                        />
                    </div>

                    <button
                        className="btn-primary register-btn"
                        type="submit"
                        disabled={
                            loading ||
                            !name.trim() ||
                            images.length === 0
                        }
                    >
                        {loading ? "Registering..." : "Register Student"}
                    </button>
                </div>
            </form>

            {message && (
                <div
                    className={`alert ${
                        message.startsWith("✅")
                            ? "alert-success"
                            : "alert-error"
                    }`}
                >
                    {message}
                </div>
            )}
        </div>
    );
}