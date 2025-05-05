import { Link, useLocation } from 'react-router-dom'
import logo from '../seme-logo.png'

function Navbar() {
    const location = useLocation();
    
    return (
        <div>
            <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                <div className="container-fluid">
                    <Link className="navbar-brand" to="/" >
                        <img src={logo} alt="Logo" style={{ height: "52px", width: 'auto' }} className="" />
                    </Link>
                    <button className="bg-dark navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                        <span className="navbar-toggler-icon"></span>
                    </button>
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                            <li className="nav-item fs-5">
                                <Link className={`nav-link ${location.pathname === './logs' ? "active" : ""}`} to="/logs">Logs</Link>
                            </li>
                            <li className="nav-item fs-5">
                                <Link className={`nav-link ${location.pathname === './devices' ? "active" : ""}`} to="/devices">Devices</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
            {/* <Alert alert={alert} /> */}
        </div>
    );
}

export default Navbar;
