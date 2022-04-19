import React, {useState} from "react";
import _ from 'lodash';
import {DndProvider} from 'react-dnd'
import {HTML5Backend} from 'react-dnd-html5-backend'
import {BoxWithHandle} from './BoxWithHandle';
import ContentBlock from './Blocks/ContentBlock';
import DropBox from "./DropBox";
import {Motion, spring} from 'react-motion';
import {isMobile} from 'react-device-detect';

export const ItemTypes = {
    BOX: 'box',
}



export default function Arena({blocks: init_blocks, block_types}) {
    if (typeof window !== 'undefined') {
        document.execCommand("defaultParagraphSeparator", false, "p");
    }

    if(init_blocks && init_blocks.length) {
        console.log("SS")
    } else {
        return <div> You have no blocks</div>
    }


    const [blocks, updateBlocks] = useState(init_blocks);
    const [last_idx, updateLastIdx] = useState(blocks[blocks.length - 1]['page_row_idx'] + 1);

    const moveBlockToIdx = (block, to_idx) => {
        /*
        Shift all Blocks after and including the insert-box by one.
         */
        let new_blocks = _.map(blocks, (blk, idx) => {
            if (blk['page_row_idx'] >= to_idx) {
                blk['page_row_idx'] += 1
            }
            return blk;
        })

        /*
        Find the block in question in the new array and set it's new index
        as the drop box.
         */
        let new_block = _.find(new_blocks, ['uid', block['uid']]);
        new_block['page_row_idx'] = to_idx;

        /*
        Update the state.
         */
        new_blocks = _.sortBy(new_blocks, ['page_row_idx']);
        updateBlocks([...new_blocks]);
        updateLastIdx(new_blocks[new_blocks.length - 1]['page_row_idx'] + 1);
    }

    const editable = !isMobile;

    return (<div>
            {editable ? <DndProvider backend={HTML5Backend}>
                    {_.map(blocks, (block, id) => (<div key={block['uid']}>
                            <DropBox className={"hide-mobile"} offset={id} key={`dropbox-${block['uid']}`}
                                     id={block['page_row_idx']}/>
                            <Motion
                                key={id}
                                style={{y: spring(id * 80, {stiffness: 10, damping: 32})}}
                            >
                                {({y}) => <BoxWithHandle offset={id} moveBlockToIdx={moveBlockToIdx}
                                                         key={`block-${block['uid']}`} block={block}
                                                         style={{
                                                             transform: 'translate3d(' + y + 'px, ' + y + 'px, 0)',
                                                         }}/>}
                            </Motion>
                        </div>))}
                    <DropBox id={last_idx} offset={blocks.length}/>
            </DndProvider> : <div style={{marginTop: '1.5rem'}}>
                {_.map(blocks, (block, id) => (
                    <ContentBlock key={block['uid']} editable={editable} block={block} className={'drop-handle'}/>))}
            </div>
            }

        </div>);
}