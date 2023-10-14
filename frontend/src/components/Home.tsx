import {Typography} from "@mui/material";
import Search from "./Search.tsx";

const Home = () => {
    return (
        <div>
            <br />
            <Typography variant={'h3'}>
                Six Degrees of Anime Characters
            </Typography>
            <br />
            <br />
            <Search />
        </div>
    )
}

export default Home

