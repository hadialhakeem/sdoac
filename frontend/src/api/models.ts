type Character = {
    mal_id: number,
    name: string,
    name_kanji: string,
    about: string,
    favorites: number,
    mal_url: string,
    img_url: string,
    nicknames: string[]
}

type Anime = {
    mal_id: number,
    favorites: number,
    title_default: string,
    titles: string[],
    mal_url: string,
    img_url: string,
    members: number,
    popularity: number,
    rank: number,

    year: number,
    scored_by: number,
    rating: string,
    synopsis: string,
    source: string,
    type: string,
    duration: string,
    score: number,
    approved: boolean,
    season: string,
    airing: false,
    episodes: number,
    status: string,
}


type Person = {
    mal_id: number,
    name: string,
    about: string,
    favorites: number,
    mal_url: string,
    img_url: string,
    alternate_names: string,
    birthday: string,
    given_name: string,
    family_name: string,
}

type Node = Character | Person | Anime

type Path = {
    nodes: Node[],
    length: number,
    degrees: number,
}

function isCharacter(node: Node): node is Character {
    return 'nicknames' in node;
}

function isAnime(node: Node): node is Anime {
    return 'members' in node;
}

function isPerson(node: Node): node is Person {
    return 'given_name' in node;
}


export type { Character, Anime, Person, Path, Node }
export { isCharacter,isAnime, isPerson }


