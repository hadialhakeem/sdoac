import {Character, isAnime, isPerson, Path} from "../api/models.ts";
import {Typography, Link, Card, CardMedia, CardContent, CardActions, Button, Box} from "@mui/material";

interface DisplayPathProps {
    path: Path
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
        <Card sx={{ display: 'flex', maxWidth: 500, border: '5px solid lightblue'}}>
            <CardMedia
                component="img"
                alt={props.title}
                image={props.img_url}
                sx={{width: 150}}
            />
            <Box>
                <CardContent sx={{textAlign: 'left'}}>
                    <Typography gutterBottom variant="h5" component="div">
                        {props.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                        {props.body}
                    </Typography>
                </CardContent>
                <CardActions>
                    <Link href={props.mal_url} target="_blank" rel="noopenner noreferrer">
                        <Button size="large">MAL</Button>
                    </Link>
                </CardActions>
            </Box>
        </Card>
    )
}


const DisplayPath = (props: DisplayPathProps) => {

    const { nodes, degrees } = props.path
    const source = nodes[0] as Character
    const dest = nodes[nodes.length - 1] as Character

    const renderNodes = nodes.map(node => {
        let rendered;

        if (isAnime(node)) {
            rendered =  <RenderNode title={node.title_default} mal_url={node.mal_url} img_url={node.img_url}
                               body={`Other Titles: ${node.titles.join(", ")}.`} />
        } else if (isPerson(node)) {
            rendered = <RenderNode title={node.name} mal_url={node.mal_url} img_url={node.img_url}
                               body={``} />
        } else {
            rendered = <RenderNode title={node.name} mal_url={node.mal_url} img_url={node.img_url}
                        body={`Also goes by ${node.nicknames.join(", ")}.`}/>
        }

        return (
            <div style={{margin: 'auto', width: '50%'}}>
                {rendered}
                <br />
                <br />
            </div>
        )
    })

    return (
        <div>
            <Typography variant="h4">
                Found a path from {source.name} to {dest.name} with {degrees} degrees of separation.
            </Typography>
            <br />
            {renderNodes}
        </div>
    )
}

export default DisplayPath