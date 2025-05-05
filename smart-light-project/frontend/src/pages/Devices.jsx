import { useEffect, useState } from "react";

const Devices = () => {
    const [devices, setDevices] = useState([]);
    const [status, setStatus] = useState({});
    const [currentPage, setCurrentPage] = useState(1);
    const devicesPerPage = 10; // You can adjust the number of devices per page

    useEffect(() => {
        fetch("http://localhost:8000/devices")
            .then((res) => res.json())
            .then((data) => setDevices(data));
    }, []);

    // Calculate the devices to display on the current page
    const indexOfLastDevice = currentPage * devicesPerPage;
    const indexOfFirstDevice = indexOfLastDevice - devicesPerPage;
    const currentDevices = devices.slice(indexOfFirstDevice, indexOfLastDevice);

    // Change page
    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    // Calculate total number of pages
    const totalPages = Math.ceil(devices.length / devicesPerPage);

    const toggleLed = (mac) => {
        const newState = status[mac] === "on" ? "off" : "on";
        fetch("http://localhost:8000/control", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mac, action: newState }),
        })
            .then(() => setStatus((prev) => ({ ...prev, [mac]: newState })));
    };

    return (
        <div className="p-4">
            <h1 className="text-xl font-bold mb-4">Connected Devices</h1>
            <table className="min-w-full table-auto border border-gray-300">
                <thead className="bg-gray-200">
                    <tr>
                        <th className="p-2 border">#</th>
                        <th className="p-2 border">MAC Address</th>
                        <th className="p-2 border">Control LED</th>
                    </tr>
                </thead>
                <tbody>
                    {currentDevices.map((device, i) => (
                        <tr key={device._id} className="text-sm">
                            <td className="border p-2">{i + 1 + indexOfFirstDevice}</td>
                            <td className="border p-2">{device.mac_address}</td>
                            <td className="border p-2">
                                <button
                                    className={`px-3 py-1 rounded text-white ${
                                        status[device.mac_address] === "on"
                                            ? "bg-green-500"
                                            : "bg-gray-500"
                                    }`}
                                    onClick={() => toggleLed(device.mac_address)}
                                >
                                    {status[device.mac_address] === "on" ? "Turn Off" : "Turn On"}
                                </button>
                            </td>
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

export default Devices;
