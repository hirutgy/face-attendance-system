import { useState } from "react";
import { registerUser } from "../api/api";

export default function Register() {
    const [name, setName] = useState("");
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleSubmit = async () => {
        if (!name || !file) {
            alert("Please enter a name and select an image");
            return;
        }

        const response = await registerUser(name, file);
        setResult(response);
    };

    return (
        <div>
            <h2>Register User</h2>

            <input
                type="text"
                placeholder="Enter name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={handleSubmit}>Register</button>

            {result && (
                <pre>{JSON.stringify(result, null, 2)}</pre>
            )}
        </div>
    );
}
