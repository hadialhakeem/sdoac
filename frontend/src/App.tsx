import {Container, Typography, Autocomplete, TextField} from "@mui/material";

function App() {
    return (
        <Container maxWidth={'lg'} sx={{textAlign: 'center'}}>
            <br />
            <Typography variant={'h3'}>
            Six Degrees of Anime Characters
            </Typography>
            <br />
            <br />
            <Autocomplete
                options={["kirito"]}
                sx={{ width: 400, float: 'left', backgroundColor: 'lightcyan' }}
                renderInput={(params) =>
                    <TextField {...params} label="Source Character" sx={{backgroundColor: 'lightcyan'}}/>}
            />


            <Autocomplete
                options={["kirito"]}
                sx={{ width: 400, float: 'right', backgroundColor: 'lightcyan' }}
                renderInput={(params) =>
                    <TextField {...params} label="Source Character" sx={{backgroundColor: 'lightcyan'}}/>}
            />

        </Container>
    )
}

export default App
