import React, { useState, useEffect, useRef } from 'react'
import { Rnd } from "react-rnd";
import {
    AiOutlineColumnWidth
} from 'react-icons/ai';

import {
    IoTrash
} from 'react-icons/io5';

function ImageBlock({editable, image_url, offset, ...props}) {

    const [imgSize, setImgSize] = useState({width: '100%'});
    const [imgPos, setImgPos] = useState({x: 0, y: 0});
    const [style, setStyle] = useState({
        position: "relative",
        display: "block",
        transform: "translate(0px, 0px)",
        margin: '0 auto',
    });

    const ref_img = useRef(null)

    useEffect(() => {
        setImgSize({
            height: ref_img.current.clientHeight,
            width: ref_img.current.clientWidth
        })
        setImgPos({x: 0, y: 0})
    }, [])

    const onResizeStart = (event, direction, refToElement) => {
        console.log(direction, refToElement)
    }

    const onResize = (event, direction, refToElement, delta, position) => {
        console.log("onResize", direction, delta, position)
        let {height : h, width : w} = imgSize;
        let {height : dh, width: dw} = delta;

        // if (direction === "right") {
        //     dw /= 2;
        //     // dh *= 2;
        //     console.log("xxxxdirection")
        // }
        //
        // setImgSize({
        //     ...imgSize,
        //     width: w + 200,
        //     height: h + dh
        // })
        //

        setImgPos({x: 0, y: 0})

        refToElement.style.transform = "translate(0px, 0px)";
    }

    const onResizeStop = (event, direction, refToElement, delta, position) => {
        console.log(event, direction, refToElement, delta, position)
        console.log(ref_img, refToElement)
        let {height : h, width : w} = imgSize;
        let {height : dh, width: dw} = delta;
        refToElement.style.transform = "translate(0px, 0px)";
        console.log(ref_img, refToElement, h/w)

        // if (direction === "right") {
        //     dw *= 2;
        //     // dh *= 2;
        //     console.log("xxxxdirection")
        // }

        setImgSize({
            width: w + dw,
            height: h + dh
        })
        setImgPos({x: 0, y: 0})
    }

    // console.log(imgSize, imgPos)

    const maximizeToWidth = () => {
        setImgSize({
            width: "100%",
            height: "100%"
        })
        setImgPos({x: 0, y: 0})
    }

    const deleteBlock = () => {
        setImgSize({
            width: "100%",
            height: "100%"
        })
        setImgPos({x: 0, y: 0})
    }

    if (editable) {
        return <div className={"image-container"}>
            <Rnd
                style={style}
                className={"react-dnd-box"}
                disableDragging
                enableResizing={{
                    top:true, right:true, bottom:true, left:true,
                    topRight:true, bottomRight:true, bottomLeft:true, topLeft:true
                }}
                lockAspectRatio
                minWidth="200px"
                maxWidth="100%"
                size={imgSize}
                position={imgPos}
                onResizeStart={onResizeStart}
                onResizeStop={onResizeStop}
                onResize={onResize}
            >
                <div className="container">
                    <img className={"resizable-image"} ref={ref_img} width={'100%'} src={image_url}/>
                    <div className="overlay hide-mobile">
                        <div className="btn-group">
                            <button onClick={() => maximizeToWidth()}><AiOutlineColumnWidth/></button>
                            <button onClick={() => deleteBlock()}><IoTrash/></button>
                        </div>
                    </div>
                </div>
            </Rnd>
        </div>
    } else {
        return <div className="container">
            <img className={"resizable-image"} ref={ref_img} width={'100%'} src={image_url}/>
        </div>
    }
}

export default ImageBlock