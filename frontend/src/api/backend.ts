import environment from "../utils/environment.ts";

import axios from "axios";
import {Character} from "./models.ts";

interface SearchCharactersResponse {
    data: Character[]
}


interface ShortestPathResponse {

}

class BackendAPI {
    static apiUrl = environment.apiUrl

    static searchCharacters = (q: string) => {
        return axios.get(`${this.apiUrl}/search?q=${q}`)
            .then<SearchCharactersResponse>(res => res.data)
    }

    static shortestPath = (srcId: number, destId: number) => {
        return axios.get(`${this.apiUrl}/path?src_id=${srcId}&dest_id=${destId}`)
            .then<ShortestPathResponse>(res => res.data)
    }


}
export { BackendAPI }

