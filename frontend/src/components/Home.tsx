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
            <Typography variant={'h5'}>
                What is this?
            </Typography>
            <Typography variant={'body1'} sx={{textAlign: "left"}}>
                Find out how connected the anime world is. Choose 2 of your favorite characters, press GO, and you'll get
                a path that will connect those 2 characters. Two characters are considered connected if,
                <ul>
                    <li>
                        They appear in the same anime or,
                    </li>
                    <li>
                        They share the same voice actor.
                    </li>
                </ul>
                With just these 2 criteria we can connect (almost) all characters.
            </Typography>
            <br />
            <br />
            <Search />
        </div>
    )
}

export default Home

