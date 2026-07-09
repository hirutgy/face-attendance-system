import "./Recognize.css";
import { useState } from "react";
import FileUpload from "../components/FileUpload/FileUpload";
import PageHeader from "../components/PageHeader/PageHeader";
import { markAttendance, recognizeUser } from "../api/api";

function Recognize() {
    const [image, setImage] = useState(null);
    const [result, setResult] = useState(null);
    const [mode, setMode] = useState("recognize");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!image) return;

        setLoading(true);
        setResult(null);
        console.log("IMAGE =", image);
        console.log("Is File?", image instanceof File);
        console.log("Type:", typeof image);
        const formData = new FormData();
        formData.append("file", image);

        try {
            const response =
                mode === "attendance"
                    ? await markAttendance(formData)
                    : await recognizeUser(formData, false);

            if (response.status === "success") {
                setResult({
                    success: true,
                    name: response.name,
                    confidence: response.confidence,
                    duplicate: response.duplicate,
                    attendanceLogged: response.attendance_logged,
                });
            } else {
                setResult({
                    success: false,
                    message:
                        response.message ||
                        response.detail ||
                        "No match found.",
                });
            }
        } catch (error) {
            console.error(error);

            setResult({
                success: false,
                message: error.message || "Unknown error occurred.",
            });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <PageHeader
                icon="📷"
                title="Face Recognition"
                subtitle="Upload a face image to recognize a registered user or record attendance."
            />

            <div className="mode-toggle">
                <label>
                    <input
                        type="radio"
                        value="recognize"
                        checked={mode === "recognize"}
                        onChange={() => setMode("recognize")}
                    />
                    Recognize Only
                </label>

                <label>
                    <input
                        type="radio"
                        value="attendance"
                        checked={mode === "attendance"}
                        onChange={() => setMode("attendance")}
                    />
                    Mark Attendance
                </label>
            </div>

            <form className="form" onSubmit={handleSubmit}>
                <div className="form-card">
                    <div className="form-section">
                        <h3>Upload Face Image</h3>

                        <FileUpload
                            multiple={false}
                            files={image}
                            onChange={(file) => {
                                console.log("received:",file)
                                setImage(file);
                            }}
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn-primary recognize-btn"
                        disabled={loading || !image}
                    >
                        {loading
                            ? "⏳ Processing..."
                            : mode === "attendance"
                            ? "✅ Mark Attendance"
                            : "🔍 Recognize Face"}
                    </button>
                </div>
            </form>

            {result && (
                <div className="result-card">
                    {result.success ? (
                        <>
                            <div className="result-avatar">
                                👤
                            </div>

                            <h2>{result.name}</h2>

                            <div className="confidence">
                                <div className="confidence-label">
                                    Confidence
                                </div>

                                <div className="confidence-bar">
                                    <div
                                        className="confidence-fill"
                                        style={{
                                            width: `${
                                                (result.confidence || 0) * 100
                                            }%`,
                                        }}
                                    />
                                </div>

                                <span>
                                    {(
                                        (result.confidence || 0) * 100
                                    ).toFixed(1)}
                                    %
                                </span>
                            </div>

                            <div className="status-badge success">
                                {result.duplicate
                                    ? "⚠️ Already Checked In Today"
                                    : result.attendanceLogged
                                    ? "✅ Attendance Recorded"
                                    : "✅ User Recognized"}
                            </div>
                        </>
                    ) : (
                        <>
                            <div className="result-avatar">❌</div>

                            <h2>No Match Found</h2>

                            <div className="status-badge error">
                                {result.message}
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
}

export default Recognize;