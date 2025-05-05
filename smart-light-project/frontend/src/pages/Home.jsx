import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-50">
            <h1 className="text-3xl font-bold text-blue-700 mb-4 text-center">Welcome to the Smart Light System</h1>
            <p className="text-gray-600 text-center max-w-xl mb-8">
                Monitor motion events, control Raspberry Pi lights remotely, and view device status in real time.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
                <Link to="/logs" className="bg-white p-6 rounded-2xl shadow hover:shadow-lg border hover:border-blue-400 transition no-underline w-full">
                    <h2 className="text-xl font-semibold text-blue-600 mb-2 text-center">📋 Motion Logs</h2>
                    <p className="text-gray-600 text-center">View a history of detected motion events from all connected devices.</p>
                </Link>

                <Link to="/devices" className="bg-white p-6 rounded-2xl shadow hover:shadow-lg border hover:border-blue-400 transition no-underline w-full">
                    <h2 className="text-xl font-semibold text-blue-600 mb-2 text-center">💡 Device Control</h2>
                    <p className="text-gray-600 text-center">See all Raspberry Pi devices and remotely toggle their LEDs.</p>
                </Link>
            </div>
        </div>
    );
};

export default Home;
