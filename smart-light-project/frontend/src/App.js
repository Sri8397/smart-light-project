import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Logs from "./pages/Logs";
import Devices from "./pages/Devices";
import Navbar from "./components/Navbar";

function App() {
    return (
        <Router>
            <Navbar />
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/logs" element={<Logs />} />
                <Route path="/devices" element={<Devices />} />
            </Routes>
        </Router>
    );
}

export default App;
