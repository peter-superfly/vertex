import React from 'react'
import { useDrop } from 'react-dnd'
import { ItemTypes } from './ItemTypes';

function DropBox({children, offset, ...props}) {
    const [{ isOver, canDrop, didDrop, _props, isDragging }, drop] = useDrop(
        () => ({
            accept: ItemTypes.BOX,
            canDrop : (item, monitor) => {
                let it = monitor.getItem()
                // Don't allow dropping of elements is this dropbox immediately
                // precedes or succeeds the current drag item.
                return Math.abs(it.offset - offset) > 1;
            },
            collect: (drop_mon, props) => ({
                isOver: !!drop_mon.isOver(),
                canDrop: !!drop_mon.canDrop(),
                didDrop: !!drop_mon.didDrop(),
                _props: props
            }),
            drop : (item, monitor) => {
                return {id : props.id }
            }
        }),
        [props.id]
    )
    return (
            <div
                ref={drop}
                style={{
                    position: 'relative',
                    margin: '10px',
                    backgroundColor: (canDrop)? "white" : "",
                    width: '100%',
                    height: '15px',
                }}
            >
                {children}
            </div>

    )
}

export default DropBox