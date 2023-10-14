import {Autocomplete, TextField} from "@mui/material";
import {useState} from "react";
import {Character} from "../api/models.ts";
import {BackendAPI} from "../api/backend.ts";

const AutocompleteCharacter = () => {
    interface CharacterOption {
        label: string
        character: Character
    }

    const [options, setOptions] = useState<CharacterOption[]>([]);
    const [search, setSearch] = useState("")

    const onInputChange = (newSearch: string) => {
        setSearch(newSearch)
        BackendAPI
            .searchCharacters(newSearch)
            .then(res => {
                const newOptions: CharacterOption[] = res.data.map(character => {
                    return {
                        label: character.name,
                        character: character
                    }
                })
                setOptions(newOptions)
            })
    }

    return(
        <Autocomplete
            inputValue={search}
            options={options}
            sx={{ width: 400, float: 'left' }}
            onInputChange={(_e, newSearch) => onInputChange(newSearch)}
            renderInput={(params) =>
                <TextField {...params} label="Source Character"/>}
        />
    )

}

export default AutocompleteCharacter
