import {Autocomplete, TextField} from "@mui/material";
import {useEffect, useState} from "react";
import {Character} from "../api/models.ts";
import {BackendAPI} from "../api/backend.ts";

const AutocompleteCharacter = () => {
    const [options, setOptions] = useState<Character[]>([]);
    const [search, setSearch] = useState("")

    const onValueChange = (newValue: Character | null) => {
        console.log(newValue)
    }

    useEffect(() => {
        const getOptions = setTimeout(() =>
            BackendAPI
            .searchCharacters(search)
            .then(res => setOptions(res.data)),
            1000)

        return () => clearTimeout(getOptions)
    }, [search])

    
    return(
        <Autocomplete
            inputValue={search}
            options={options}
            sx={{ width: 400, float: 'left' }}
            onInputChange={(_e, newSearch) => setSearch(newSearch)}
            onChange = {(_e, newValue) => onValueChange(newValue)}

            isOptionEqualToValue={(option, value) =>
                option.mal_id === value.mal_id}

            renderInput={(params) =>
                <TextField {...params} label="Source Character"/>}
            filterOptions={x => x}
            getOptionLabel={option => option.name || ""}

            renderOption={(props, option, state, ownerState) =>{
                console.log({state})
                console.log({ownerState})
                return (
                    <li {...props} key={option.mal_id}>
                        {option.name}
                    </li>
                )
            }}
        />
    )

}

export default AutocompleteCharacter
