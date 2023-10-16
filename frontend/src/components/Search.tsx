import AutocompleteCharacter from "./AutocompleteCharacter.tsx";
import {useState} from "react";
import {BackendAPI} from "../api/backend.ts";
import {Button} from "@mui/material";
import {Character, Path} from "../api/models.ts";
import DisplayPath from "./DisplayPath.tsx";


const Search = () => {
    const [source, setSource] = useState<Character | null>(null);
    const [dest, setDest] = useState<Character | null>(null);
    const [path, setPath] = useState<Path | null>(null)

    const [loading, setLoading] = useState(false)

    const onGoClick = () => {

        if (source == null || dest == null) {
            return
        }

        setLoading(true)
        BackendAPI
            .shortestPath(source.mal_id, dest.mal_id)
            .then(res => {
                console.log(res)
                setPath(res.path)
            })
            .finally(() => {
                setLoading(false)
            })
    }

    return (
        <div>
            <AutocompleteCharacter textLabel={'Source Character'} setValueCB={setSource} />
            <AutocompleteCharacter textLabel={'Destination Character'} setValueCB={setDest}
                                   floatRight />
            <br />
            <br />
            <br />
            <div>
                <img src={source?.img_url} alt={source?.name} style={{width: 100}}/>
                <img src={dest?.img_url} alt={dest?.name} style={{width: 100}}/>
            </div>
            <br />
            <br />
            <Button color="secondary" disabled={loading}
                    variant="contained" size="large"
                    onClick={onGoClick}>
                GO!!
            </Button>
            <br />
            <br />
            <br />
            {path && <DisplayPath path={path} />}
        </div>
    )
}

export default Search
