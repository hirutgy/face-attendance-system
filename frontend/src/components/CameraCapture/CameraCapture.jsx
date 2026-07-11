import { useEffect, useRef, useState } from "react";
import "./CameraCapture.css";

function createCaptureFile(blob) {
    const stamp = new Date().toISOString().replace(/[:.]/g, "-");
    return new File([blob], `camera-${stamp}.jpg`, {
        type: "image/jpeg",
        lastModified: Date.now(),
    });
}

export default function CameraCapture({
    onCapture,
    disabled = false,
    facingMode = "user",
}) {
    const videoRef = useRef(null);
    const streamRef = useRef(null);
    const [active, setActive] = useState(false);
    const [error, setError] = useState("");
    const [capturing, setCapturing] = useState(false);

    const stopCamera = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => track.stop());
            streamRef.current = null;
        }
        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
        setActive(false);
    };

    const startCamera = async () => {
        if (disabled) return;

        setError("");

        if (!navigator.mediaDevices?.getUserMedia) {
            setError("Camera is not supported in this browser.");
            return;
        }

        try {
            stopCamera();

            // ⭐ Edge-safe camera selection
            const devices = await navigator.mediaDevices.enumerateDevices();
            const camera = devices.find((d) => d.kind === "videoinput");

            if (!camera) {
                setError("No camera device found.");
                return;
            }

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: { deviceId: camera.deviceId }, // ⭐ FIXED for Edge
            });

            streamRef.current = stream;

            if (videoRef.current) {
                videoRef.current.srcObject = stream;

                // ⭐ Edge requires metadata before play()
                await new Promise((resolve) => {
                    videoRef.current.onloadedmetadata = resolve;
                });

                await videoRef.current.play();
            }

            setActive(true);
        } catch (err) {
            console.error(err);
            setError(
                err?.name === "NotAllowedError"
                    ? "Camera permission denied. Allow access and try again."
                    : "Unable to open the camera. Check permissions and try again."
            );
            stopCamera();
        }
    };

    useEffect(() => {
        return () => {
            stopCamera();
        };
    }, []);

    const takePhoto = async () => {
        const video = videoRef.current;
        if (!video || !active || disabled) return;

        setCapturing(true);

        try {
            const width = video.videoWidth || 640;
            const height = video.videoHeight || 480;
            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext("2d");
            ctx.drawImage(video, 0, 0, width, height);

            const blob = await new Promise((resolve, reject) => {
                canvas.toBlob(
                    (result) => {
                        if (result) resolve(result);
                        else reject(new Error("Failed to capture frame"));
                    },
                    "image/jpeg",
                    0.92
                );
            });

            onCapture(createCaptureFile(blob));
        } catch (err) {
            console.error(err);
            setError("Could not capture photo. Please try again.");
        } finally {
            setCapturing(false);
        }
    };

    return (
        <div className="camera-capture">
            <div className="camera-preview">
                {active ? (
                    <video
                        ref={videoRef}
                        className="camera-video"
                        playsInline
                        muted
                        autoPlay
                    />
                ) : (
                    <div className="camera-placeholder">
                        <div className="camera-placeholder-icon">📷</div>
                        <p>Start the camera to take a face photo</p>
                    </div>
                )}
            </div>

            <div className="camera-actions">
                {!active ? (
                    <button
                        type="button"
                        className="camera-btn primary"
                        onClick={startCamera}
                        disabled={disabled}
                    >
                        Start Camera
                    </button>
                ) : (
                    <>
                        <button
                            type="button"
                            className="camera-btn primary"
                            onClick={takePhoto}
                            disabled={disabled || capturing}
                        >
                            {capturing ? "Capturing…" : "Capture Photo"}
                        </button>
                        <button
                            type="button"
                            className="camera-btn secondary"
                            onClick={stopCamera}
                            disabled={disabled}
                        >
                            Stop Camera
                        </button>
                    </>
                )}
            </div>

            {error && <div className="camera-error">{error}</div>}

            <small className="camera-hint">
                Use a clear, front-facing view with good lighting.
            </small>
        </div>
    );
}
