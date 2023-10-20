import {Anime, Character, isAnime, isPerson, Path, Person} from "../api/models.ts";
import {Typography, Link, Card, CardMedia, CardContent, CardActions, Button} from "@mui/material";
import { ReactNode } from "react"

interface DisplayPathProps {
    path: Path
}

const RenderCharacter = (props: { character: Character }) => {
    const { character } = props

    return (
        <div>
            <img src={character.img_url} alt={character.name} style={{width: 150, float: "left"}} />
            <Typography variant={'body1'} sx={{textAlign: "left"}}>
                <Link href={character.mal_url} target="_blank" rel="noopenner noreferrer">
                    {character.name}
                </Link>
                <br />
                Also goes by {character.nicknames.join(", ")}.
            </Typography>
            <div style={{clear: "both"}} />
        </div>
    )
}

const RenderPerson = (props: { person: Person }) => {
    const { person } = props

    return (
        <div>
            <img src={person.img_url} alt={person.name} style={{width: 150, float: "left"}} />
            <Typography variant={'body1'} sx={{textAlign: "left"}}>
                <Link href={person.mal_url} target="_blank" rel="noopenner noreferrer">
                    {person.name}
                </Link>
                <br />
            </Typography>
            <div style={{clear: "both"}} />
        </div>
    )
}

interface RenderNodeProps {
    title: string
    body: string
    img_url: string
    mal_url: string
    img_class?: string
}

const RenderNode = (props: RenderNodeProps) => {

    return (
        <Card sx={{ maxWidth: 345 }}>
            <CardMedia
                component="img"
                alt={props.title}
                width={150}
                image={props.img_url}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                    {props.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    {props.body}
                </Typography>
            </CardContent>
            <CardActions>
                <Link href={props.mal_url} target="_blank" rel="noopenner noreferrer">
                    <Button size="small">MAL</Button>
                </Link>
            </CardActions>
        </Card>
    )
}

const RenderAnime = (props: { anime: Anime }) => {
    const { anime } = props

    return (
        <div>
            <img src={anime.img_url} alt={anime.title_default} style={{width: 150, float: "left"}} />
            <Typography variant={'body1'} sx={{textAlign: "left"}}>
                <Link href={anime.mal_url} target="_blank" rel="noopenner noreferrer">
                    {anime.title_default}
                </Link>
                <br />
                Other Titles: {anime.titles.join(", ")}.
            </Typography>
            <div style={{clear: "both"}} />
        </div>
    )
}


const DisplayPath = (props: DisplayPathProps) => {

    const { nodes, length, degrees } = props.path

    const renderNodes = nodes.map(node => {
        if (isAnime(node)) return <RenderAnime anime={node} />
        if (isPerson(node)) return <RenderPerson person={node} />
        return <RenderCharacter character={node} />
    })

    const renderNodesB = nodes.map(node => {
        if (isAnime(node)) {
            return <RenderNode title={node.title_default} mal_url={node.mal_url} img_url={node.img_url}
                               body={`Other Titles: ${node.titles.join(", ")}.`} />
        }
        if (isPerson(node)) {
            return <RenderNode title={node.name} mal_url={node.mal_url} img_url={node.img_url}
                               body={``} />
        }
        return <RenderNode title={node.name} mal_url={node.mal_url} img_url={node.img_url}
                           body={`Also goes by ${node.nicknames.join(", ")}.`} />
    })

    return (
        <div>
            {renderNodesB}
            <br />
            <hr />
            <br />
            {renderNodes}
        </div>
    )
}

export default DisplayPath