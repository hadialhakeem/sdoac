import {Autocomplete, TextField} from "@mui/material";
import {useEffect, useState} from "react";
import {Character} from "../api/models.ts";
import {BackendAPI} from "../api/backend.ts";

interface AutocompleteCharacterProps {
    textLabel: string
    floatRight?: boolean
    setValueCB?: (character: Character | null) => void
}

const AutocompleteCharacter = (props: AutocompleteCharacterProps) => {
    const [options, setOptions] = useState<Character[]>([]);
    const [search, setSearch] = useState("")

    const onValueChange = (newValue: Character | null) => {
        if (props.setValueCB) props.setValueCB(newValue)
    }

    useEffect(() => {
        const getOptions = setTimeout(() =>
            BackendAPI
            .searchCharacters(search)
            .then(res => setOptions(res.data)),
            500)

        return () => clearTimeout(getOptions)
    }, [search])

    let float = 'left';
    if (props.floatRight) float = 'right';
    
    return(
        <Autocomplete
            inputValue={search}
            options={options}
            sx={{ width: 400, float: float }}
            onInputChange={(_e, newSearch) => setSearch(newSearch)}
            onChange = {(_e, newValue) => onValueChange(newValue)}

            isOptionEqualToValue={(option, value) =>
                option.mal_id === value.mal_id}

            renderInput={(params) =>
                <TextField {...params} label={props.textLabel} />}
            filterOptions={x => x}
            getOptionLabel={option => option.name || ""}

            renderOption={(props, option, state, ownerState) =>{
                console.log({state})
                console.log({ownerState})
                return (
                    <li {...props} key={option.mal_id}>
                        <img src={option.img_url} alt={option.name} style={{
                            width: 40,
                        }}/>&nbsp;&nbsp;&nbsp;{option.name}
                    </li>
                )
            }}
        />
    )

}

export default AutocompleteCharacter
