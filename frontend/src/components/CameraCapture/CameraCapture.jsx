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

    const stopTracks = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach((track) => track.stop());
            streamRef.current = null;
        }
    };

    const stopCamera = () => {
        stopTracks();
        if (videoRef.current) {
            videoRef.current.srcObject = null;
        }
        setActive(false);
    };

    // Attach stream after the video element is mounted
    useEffect(() => {
        const video = videoRef.current;
        const stream = streamRef.current;

        if (!active || !video || !stream) return;

        video.srcObject = stream;
        const playPromise = video.play();
        if (playPromise?.catch) {
            playPromise.catch((err) => {
                console.error(err);
                setError("Unable to play camera preview. Try again.");
            });
        }

        return () => {
            video.srcObject = null;
        };
    }, [active]);

    useEffect(() => {
        return () => {
            stopTracks();
        };
    }, []);

    const startCamera = async () => {
        if (disabled) return;

        setError("");

        if (!window.isSecureContext && location.hostname !== "localhost") {
            setError(
                "Camera requires HTTPS or localhost. Open the app via http://localhost:5173.",
            );
            return;
        }

        if (!navigator.mediaDevices?.getUserMedia) {
            setError("Camera is not supported in this browser.");
            return;
        }

        try {
            stopTracks();
            if (videoRef.current) {
                videoRef.current.srcObject = null;
            }

            const stream = await navigator.mediaDevices.getUserMedia({
                audio: false,
                video: {
                    facingMode: { ideal: facingMode },
                    width: { ideal: 1280 },
                    height: { ideal: 720 },
                },
            });

            streamRef.current = stream;
            setActive(true);
        } catch (err) {
            console.error(err);
            stopTracks();
            setActive(false);

            if (err?.name === "NotAllowedError" || err?.name === "PermissionDeniedError") {
                setError("Camera permission denied. Allow access and try again.");
            } else if (err?.name === "NotFoundError" || err?.name === "DevicesNotFoundError") {
                setError("No camera was found on this device.");
            } else {
                setError("Unable to open the camera. Check permissions and try again.");
            }
        }
    };

    const waitForFrame = (video) =>
        new Promise((resolve, reject) => {
            if (video.videoWidth > 0 && video.videoHeight > 0) {
                resolve();
                return;
            }

            const timeout = setTimeout(() => {
                cleanup();
                reject(new Error("Camera is not ready yet"));
            }, 4000);

            const onReady = () => {
                if (video.videoWidth > 0) {
                    cleanup();
                    resolve();
                }
            };

            const cleanup = () => {
                clearTimeout(timeout);
                video.removeEventListener("loadeddata", onReady);
                video.removeEventListener("loadedmetadata", onReady);
            };

            video.addEventListener("loadeddata", onReady);
            video.addEventListener("loadedmetadata", onReady);
        });

    const takePhoto = async () => {
        const video = videoRef.current;
        if (!video || !active || disabled) return;

        setCapturing(true);
        setError("");

        try {
            await waitForFrame(video);

            const width = video.videoWidth;
            const height = video.videoHeight;
            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;

            const ctx = canvas.getContext("2d");
            // Match mirrored preview so the saved photo looks the same
            ctx.translate(width, 0);
            ctx.scale(-1, 1);
            ctx.drawImage(video, 0, 0, width, height);

            const blob = await new Promise((resolve, reject) => {
                canvas.toBlob(
                    (result) => {
                        if (result) resolve(result);
                        else reject(new Error("Failed to capture frame"));
                    },
                    "image/jpeg",
                    0.92,
                );
            });

            onCapture(createCaptureFile(blob));
        } catch (err) {
            console.error(err);
            setError("Could not capture photo. Wait for the preview, then try again.");
        } finally {
            setCapturing(false);
        }
    };

    return (
        <div className="camera-capture">
            <div className={`camera-preview ${active ? "is-active" : ""}`}>
                <video
                    ref={videoRef}
                    className="camera-video"
                    playsInline
                    muted
                    autoPlay
                    style={{ display: active ? "block" : "none" }}
                />

                {!active && (
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
                Use a clear, front-facing view with good lighting. Prefer
                http://localhost:5173 so the browser allows camera access.
            </small>
        </div>
    );
}
