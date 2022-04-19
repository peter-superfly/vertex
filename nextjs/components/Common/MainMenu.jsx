import React, {useState, useEffect} from 'react';
import Link from 'next/link'
import {ReactComponent as ReactLogo} from './logo.svg';


import {
    GiAnvilImpact,
    GiSandCastle,
    GiDesk
} from 'react-icons/gi';
import {
    MdMapsHomeWork
} from 'react-icons/md';

import {
    FaUserAstronaut, FaChessKnight
} from 'react-icons/fa';

import {
    IoRocket
} from 'react-icons/io5';

import {
    AiOutlineLogin
} from 'react-icons/ai';


function MainLogo({}) {
    console.log(ReactLogo)
    return (
        <div className={'main-logo'}>
            <Link href="/">
                <svg fill="white" id="a" viewBox="0 0 4000 4000" xmlns="http://www.w3.org/2000/svg">
                    <g>
                        <circle cx="2800" cy="1300" r="500" fill="currentColor"/>
                        <path d="M 1080.824 1814.257 C 1054.884 1807.677 1029.454 1799.057 1004.814 1788.497 L 1004.694 1788.437 C 907.574 1746.697 822.593 1674.397 765.683 1575.826 C 625.393 1332.765 708.693 1021.944 951.694 881.634 C 1194.715 741.322 1505.557 824.624 1645.887 1067.644 C 1702.777 1166.214 1722.897 1275.995 1710.517 1380.955 L 1710.517 1380.935 L 1710.477 1381.075 C 1707.357 1407.715 1702.077 1434.025 1694.797 1459.825 C 1621.577 1856.567 1728.857 2042.407 2109.079 2177.358 C 2135.019 2183.938 2160.459 2192.518 2185.089 2203.118 L 2185.229 2203.158 L 2185.209 2203.178 C 2282.309 2244.918 2367.329 2317.229 2424.249 2415.768 C 2564.549 2658.809 2481.259 2969.668 2238.199 3109.98 C 1995.199 3250.27 1684.377 3166.99 1544.047 2923.968 C 1487.137 2825.399 1466.997 2715.659 1479.397 2610.659 L 1479.437 2610.539 C 1482.577 2583.919 1487.877 2557.599 1495.137 2531.828 C 1568.377 2135.068 1461.057 1949.217 1080.834 1814.257" transform="matrix(0.999987, 0.00504, -0.00504, 0.999987, 10.079104, -8.013302)"
                              style={{fill: 'currentColor'}}/>
                    </g>
                </svg>
            </Link>
        </div>)
}

function MainMenu(props) {
    return (<div className="main-menu">
        <MainLogo/>
        <hr className="rounded"/>
        <Link href={"/people"}>
            <div className={'main-menu-icons'}>
                <FaUserAstronaut size={"2.5rem"}/>
                <br/>
                <span>People</span>
            </div>
        </Link>
        <Link href={"/companies"}>
            <div className={'main-menu-icons'}>
                <MdMapsHomeWork size={"2.5rem"}/>
                <br/>
                <span>Companies</span>
            </div>
        </Link>
        <Link href={"/jobs"}>
            <div className={'main-menu-icons'}>
                <GiDesk size={"2.5rem"}/>
                <br/>
                <span>Jobs</span>
            </div>
        </Link>
        {/*
        <Link href={"/workbench"}>
            <div className={'main-menu-icons'}>
                <GiAnvilImpact size={"2.5rem"}/>
                <br/>
                <span>Workbench</span>
            </div>
        </Link>
        <Link href={"/workbench"}>
            <div className={'main-menu-icons'}>
                <IoRocket size={"2.5rem"}/>
                <br/>
                <span>Launch</span>
            </div>
        </Link>
        */}
        <Link href={"/login"}>
            <div className={'main-menu-icons'}>
                <AiOutlineLogin size={"2.5rem"}/>
                <br/>
                <span>Login</span>
            </div>
        </Link>
    </div>);
}

export default MainMenu;
