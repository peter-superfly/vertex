import {useDrag} from 'react-dnd';
import React, {useState} from "react";

import {ItemTypes} from './ItemTypes';
import {Popover} from 'react-tiny-popover'
import {SetBlockRowIdx, UpdateAccount} from "../lib/sharedQueries";
import {useMutation, useQuery} from "@apollo/client";
import {IncrementBlockRowIdx, EditBlockText, InsertBlock} from "../lib/sharedQueries";
import ContentBlock from './Blocks/ContentBlock';

export const BoxWithHandle = ({block, offset, moveBlockToIdx, y, ...rest}) => {
    const [incBlockIdx] = useMutation(IncrementBlockRowIdx);
    const [editBlockText] = useMutation(EditBlockText);
    const [setBlockRowIdx] = useMutation(SetBlockRowIdx);
    const [insertBlock] = useMutation(InsertBlock);
    const [isPopoverOpen, setIsPopoverOpen] = useState(false);
    const [collected, drag, preview] = useDrag(() => ({
        type: ItemTypes.BOX,
        item: {...block, offset},
        collect: (drag_mon) => ({
            isDragging: drag_mon.isDragging(),
            opacity: drag_mon.isDragging(),
            dropRes: drag_mon.getDropResult(),
            getInitialClientOffset: drag_mon.getInitialClientOffset()
        }),
        end : async (item, monitor) => {
            if (monitor.didDrop()) {
                let res = monitor.getDropResult();
                let {id : dropbox_id} = res;
                let variables = {
                    "owner_uid": item['owner_uid'],
                    "page_row_idx": dropbox_id
                }
                moveBlockToIdx(item, dropbox_id)
                await incBlockIdx({variables})

                variables = {
                    "uid": item['uid'],
                    "page_row_idx": dropbox_id
                }
                await setBlockRowIdx({variables})
            }

        }
    }), block.uid);

    const clickPopOver = () => {
        console.log("clickPopOver")
    }

    const editTask = (x, e) => {
        console.log("editTask", x, e.currentTarget.textContent)
        let variables = {
            "uid": block['uid'],
            "text": e.currentTarget.textContent
        }
        editBlockText({variables})
    }

    const  _insertBlock = async (b) => {
        console.log("insertBlock", b)

        let variables = {
            "owner_uid": b['owner_uid'],
            "page_row_idx": b['page_row_idx']
        }

        await incBlockIdx({variables})

        variables = {
            "owner_uid": b['owner_uid'],
            "type": 1,
            "page_row_idx": b['page_row_idx']
        }
        await insertBlock({variables})

    }

    let {opacity, isDragging, dropRes, getInitialClientOffset} = collected;
    return (<Popover
        ref={preview}
        isOpen={isPopoverOpen}
        positions={['top', 'bottom', 'left', 'right']} // preferred positions by priority
        content={<div>Hi! I'm popover content.</div>}
        onClick={() => clickPopOver()}
    >
        <div ref={preview} style={{
            zIndex: isDragging ?  2 : 1,
            display: 'flex'
        }}
             onClick={() => setIsPopoverOpen(!isPopoverOpen)}
             // onMouseOver={() => setIsPopoverOpen(true)}
             // onMouseOut={() => setIsPopoverOpen(false)}
        >
            <div className={'drop-handle hide-mobile'} onClick={() => _insertBlock(block)} />
            <div className={'drop-handle hide-mobile'}  ref={drag}/>
            <ContentBlock block={block} className={'drop-handle'}/>

            {/*<p>{block.text}</p>*/}

        </div>
    </Popover>);
};
