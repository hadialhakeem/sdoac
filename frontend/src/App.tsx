import {Container, Typography, Autocomplete, TextField} from "@mui/material";

function App() {
    return (
        <Container maxWidth={'md'} sx={{textAlign: 'center'}}>
            <br />
            <Typography variant={'h3'}>
            Six Degrees of Anime Characters
            </Typography>
            <br />
            <br />
            <Autocomplete
                options={["kirito"]}
                sx={{ width: 400, float: 'left' }}
                renderInput={(params) =>
                    <TextField {...params} label="Source Character" sx={{backgroundColor: 'white'}}/>}
            />


            <Autocomplete
                options={["kirito"]}
                sx={{ width: 400, float: 'right' }}
                renderInput={(params) =>
                    <TextField {...params} label="Source Character" sx={{backgroundColor: 'white'}}/>}
            />

        </Container>
    )
}

export default App
