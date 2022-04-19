import React, {useState, useEffect} from 'react';
import Link from 'next/link'
import _ from 'lodash';
import {getLS} from "../lib/ls";
import {
    IoCalendarClearOutline,
    IoLogoDribbble,
    IoLogoInstagram,
    IoLogoLinkedin,
    IoLogoTwitter,
    IoMailOutline,
    IoLogoGithub,
    IoLogoFacebook,
    IoLogoTwitch,
    IoPhonePortraitOutline
} from 'react-icons/io5';

import {FaPenAlt} from 'react-icons/fa';

function JoinDate({created_at}) {
    let join_date = new Date(created_at)
    let date_options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    let date_str = join_date.toLocaleDateString("en-US", date_options);

    return <p className={'text-left'}><IoCalendarClearOutline/>&nbsp;Joined on {date_str}</p>
}

function SocialCards({social_list}) {
    const navToSocialLink = () => {
        window.open('http://github.com', '_blank');
    }

    return <div className={"social-card-container"}>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoInstagram/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoTwitter/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoFacebook/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoDribbble/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoLinkedin/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoTwitch/></p>
        <p onClick={navToSocialLink} className={'social-icon'}><IoLogoGithub/></p>
    </div>
}

function ProfileCard(props) {
    const {profile, blocks, block_types, themes, ...rest} = props

    let theme_key = _.find(themes, ['id', profile['theme']])
    if (theme_key) {
        theme_key = theme_key['key']
    }

    const [clicked, setClicked] = useState(false);

    const [image, setImage] = useState(true);
    const [toggled, setToggled] = useState(false);

    const handleCollapsedChange = (checked) => {
        setCollapsed(checked);
    };

    let logged_in_user = getLS('user')
    let can_edit_profile = logged_in_user && (logged_in_user['uid'] === profile['uid'])

    return (<div className="user-card-centered">
        <div className="card-header">

            {/*<Player className="video-banner" style={{padding: "0px"}} muted autoPlay controls={false}>*/}
            {/*    <source src="/production_ID_4722967.mp4" />*/}
            {/*</Player>*/}
            <img className="profile-banner"
                 src={profile['banner_url']}/>
            <img className="profile-avatar"
                 src={profile['avatar_url']}/>
            {
                can_edit_profile && (<div className="overlay-edit-profile hide-mobile">
                    <Link href={"/account/edit"}><div><FaPenAlt/>&nbsp;Edit</div></Link>
                </div>)
            }

        </div>

        <div className="card-body">

            <h3>{profile.fullname}</h3>
            <h5>{profile.title}</h5>
            {profile.location && <p className={'text-left'}><IoPhonePortraitOutline/>&nbsp;{profile.location}</p>}
            <JoinDate created_at={profile['created_at']}/>
            {profile.phone && <p className={'text-left'}><IoPhonePortraitOutline/>&nbsp;{profile.phone}</p>}
            {profile.email && <p className={'text-left'}><IoMailOutline/>&nbsp;{profile.email}</p>}
            <SocialCards />
            <p>{profile.bio}</p>

        </div>
    </div>);
}

export default ProfileCard;
