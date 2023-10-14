import {
    createBrowserRouter,
    RouterProvider,
} from "react-router-dom";
import Home from "./components/Home.tsx";
import {Container} from "@mui/material";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
    },
]);


const App = () => {
    return (
        <Container maxWidth={'md'} sx={{textAlign: 'center'}}>
            <RouterProvider router={router} />
        </Container>
    )
}

export default App
