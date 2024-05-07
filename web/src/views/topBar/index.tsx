import {
    ReactElement,
    useContext,
    useEffect,
    useRef,
    useState
} from "react";

import userDataContext from "context/userData";

import "./index.scss";

export default function TopBar(): ReactElement {
    const menuRef = useRef<HTMLDivElement>(null);

    const [superice, setSuperice] = useState<boolean>(false);
    const [open, setOpen] = useState<boolean>(false);
    const [menuSize, setMenuSize] = useState<Array<number>>([0, 0]);

    const userData = useContext(userDataContext);

    useEffect(() => {
        if (menuRef.current === null) return;
        setMenuSize([
            menuRef.current.clientWidth || 0,
            menuRef.current.clientHeight || 0,
        ]);
    }, [open, menuRef]);

    return <div id="topBar">
        <div className="title">
            <h2 onClick={() => setSuperice(true)}>Colten Pancake Stock</h2>
            <h2 className={superice ? "duck" : undefined}>{superice ? "Duck Pancake Stock" : undefined}</h2>
        </div>
        <div className="menu" data-open={open}>
            {
                userData === undefined ? <div className="button">
                    <span className="ms">login</span>
                    <span className="text">Login</span>
                </div> : <div className="button">
                    <span className="ms">menu</span>
                    <span className="text">Menu</span>
                </div>
            }
            <div className="mask">
                {
                    userData !== undefined ? <div className="content">
                        <a></a>
                    </div> : undefined
                }
            </div>
        </div>
    </div>;
};
