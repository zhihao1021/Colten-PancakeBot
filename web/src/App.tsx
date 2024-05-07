import userDataContext from "context/userData";
import { jwtDecode } from "jwt-decode";
import {
    ReactElement,
    useMemo
} from "react";
import {
    Routes
} from "react-router-dom";

import UserData from "schemas/userData";

import TopBar from "views/topBar";

export default function App(): ReactElement {
    // Get user data
    const token = localStorage.getItem("access_token");
    const userData = useMemo(() => {
        if (token === null) return undefined;
        try {
            return jwtDecode(token) as UserData;
        }
        catch {
            return undefined;
        }
    }, [token]);

    return <div id="app">
        <userDataContext.Provider value={userData}>
            <TopBar />
            <Routes>

            </Routes>
        </userDataContext.Provider>
    </div>
};
