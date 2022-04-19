import ImageBlock from "./Image";

const ContentBlock = ({block, editable}) => {
    let block_type = block['type']
    switch (block_type) {
        case 1:
            return <div className={'text-block'}>
                <p>{block.text}</p>
            </div>
        case 5:
            return <ImageBlock editable={editable} image_url={block['image_url']}/>
        default:
            return <div>Unknown</div>
    }
}

export default ContentBlock