import { useEffect, useState } from "react";

const Logs = () => {
    const [logs, setLogs] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const logsPerPage = 10; // You can adjust this number to show more/less logs per page

    useEffect(() => {
        fetch("http://localhost:8000/logs")
            .then((res) => res.json())
            // sort the logs by timestamp in descending order
            .then((data) => setLogs(data.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))))
    }, []);

    // Calculate the logs to display on the current page
    const indexOfLastLog = currentPage * logsPerPage;
    const indexOfFirstLog = indexOfLastLog - logsPerPage;
    const currentLogs = logs.slice(indexOfFirstLog, indexOfLastLog);

    // Change page
    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    // Calculate total number of pages
    const totalPages = Math.ceil(logs.length / logsPerPage);

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Motion Logs</h1>
            <table className="min-w-full table-auto border border-gray-300">
                <thead className="bg-gray-200">
                    <tr>
                        <th className="p-2 border">#</th>
                        <th className="p-2 border">MAC Address</th>
                        <th className="p-2 border">Event</th>
                        <th className="p-2 border">Timestamp</th>
                    </tr>
                </thead>
                <tbody>
                    {currentLogs.map((log, i) => (
                        <tr key={log._id} className="text-sm">
                            <td className="border p-2">{i + 1 + indexOfFirstLog}</td>
                            <td className="border p-2">{log.mac_address}</td>
                            <td className="border p-2">{log.event}</td>
                            <td className="border p-2">{new Date(log.timestamp).toLocaleString()}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {/* Pagination Controls */}
            <div className="mt-4 flex justify-center space-x-2">
                <button 
                    onClick={() => paginate(1)} 
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                    disabled={currentPage === 1}
                >
                    First
                </button>
                <button 
                    onClick={() => paginate(currentPage - 1)} 
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                    disabled={currentPage === 1}
                >
                    Previous
                </button>
                <span className="flex items-center justify-center px-4 py-2">
                    Page {currentPage} of {totalPages}
                </span>
                <button 
                    onClick={() => paginate(currentPage + 1)} 
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                    disabled={currentPage === totalPages}
                >
                    Next
                </button>
                <button 
                    onClick={() => paginate(totalPages)} 
                    className="px-4 py-2 bg-blue-500 text-white rounded disabled:opacity-50"
                    disabled={currentPage === totalPages}
                >
                    Last
                </button>
            </div>
        </div>
    );
};

export default Logs;
