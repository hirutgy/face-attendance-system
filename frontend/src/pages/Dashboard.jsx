import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageHeader from "../components/PageHeader/PageHeader";
import {
    fetchAttendance,
    fetchAnalytics,
    fetchUsers,
} from "../api/api";
import "./Dashboard.css";

function Dashboard() {
    const [attendance, setAttendance] = useState([]);
    const [analytics, setAnalytics] = useState(null);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");

    useEffect(() => {
        async function load() {
            try {
                const attendanceData = await fetchAttendance();
                const analyticsData = await fetchAnalytics();
                const usersData = await fetchUsers();

                setAttendance(attendanceData.records || []);
                setAnalytics(analyticsData);

                setUsers(
                    Array.isArray(usersData)
                        ? usersData
                        : usersData.users || usersData.records || []
                );
            } catch (error) {
                console.error("Error fetching dashboard data:", error);
            } finally {
                setLoading(false);
            }
        }

        load();
    }, []);

    const filteredAttendance = useMemo(() => {
        return attendance.filter((record) =>
            record.name.toLowerCase().includes(search.toLowerCase())
        );
    }, [attendance, search]);

    const uniqueUsers = users.length;

    const totalAttendance =
        analytics?.total_attendance_records ??
        analytics?.total_attendance ??
        attendance.length;

    const averageConfidence =
        analytics?.average_confidence !== undefined
            ? Number(analytics.average_confidence).toFixed(2)
            : attendance.length > 0
            ? (
                  attendance.reduce(
                      (sum, record) => sum + (record.confidence || 0),
                      0
                  ) / attendance.length
              ).toFixed(2)
            : "0.00";

    return (
        <div className="container dashboard-page">
            <PageHeader
                icon="📊"
                title="Attendance Dashboard"
                subtitle="Monitor attendance records, recognition confidence, and registered users."
            />

            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon">👥</div>
                    <h3>{uniqueUsers}</h3>
                    <p>Registered Users</p>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">✅</div>
                    <h3>{totalAttendance}</h3>
                    <p>Total Attendance</p>
                </div>

                <div className="stat-card">
                    <div className="stat-icon">🎯</div>
                    <h3>{averageConfidence}%</h3>
                    <p>Average Confidence</p>
                </div>
            </div>

            <div className="dashboard-search">
                <input
                    type="text"
                    placeholder="Search by name..."
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>

            {loading && (
                <div className="dashboard-empty">
                    <h3>Loading attendance...</h3>
                </div>
            )}

            {!loading && filteredAttendance.length === 0 && (
                <div className="dashboard-empty">
                    <h3>No attendance records found</h3>
                    <p>
                        Attendance records will appear here after recognition.
                    </p>
                </div>
            )}

            {!loading && filteredAttendance.length > 0 && (
                <div className="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Time</th>
                                <th>Status</th>
                                <th>Confidence</th>
                                <th>Profile</th>
                            </tr>
                        </thead>

                        <tbody>
                            {filteredAttendance.map((record) => (
                                <tr key={`${record.user_id}-${record.time}`}>
                                    <td>{record.name}</td>
                                    <td>{record.time}</td>
                                    <td>
                                        <span className="dashboard-status">
                                            {record.status}
                                        </span>
                                    </td>
                                    <td>
                                        {(record.confidence ?? 0).toFixed(2)}%
                                    </td>
                                    <td>
                                        <Link
                                            className="profile-link"
                                            to={`/profile/${record.user_id}`}
                                        >
                                            View
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}

export default Dashboard;