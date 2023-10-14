import AutocompleteCharacter from "./AutocompleteCharacter.tsx";


const Search = () => {
    return (
        <div>
            <AutocompleteCharacter textLabel={'Source Character'} />
            <AutocompleteCharacter textLabel={'Destination Character'} floatRight />
            <br/>
            <br />
        </div>
    )
}

export default Search
