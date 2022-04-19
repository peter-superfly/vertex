import { useState } from "react";

import * as EG from "evergreen-ui";

import {
  Tab,
  TabNavigation,
  Checkbox,
  Spinner,
  SideSheet,
  Dialog,
  Pane,
  Heading,
  Paragraph,
  Tablist,
  Card,
  toaster,
} from "evergreen-ui";

export default ({
  media,
  description,
  display_url,
  setSelected,
  uid,
  ...rest
}) => {
  const [_selected, _setSelected] = useState(media.selected);

  if (_selected !== media.selected) {
    _setSelected(media.selected);
  }

  const selectCheckBox = (e) => {
    _setSelected(e.target.checked);
    setSelected({ uid: media.uid, selected: e.target.checked });
  };

  return (
    <EG.Card className="content_card_box" elevation={_selected ? 4 : 1}>
      <Pane className="content_card_wrapper">
        <div className="rect-img-container">
          <img className="rect-img" src={media.display_url} alt="" />
        </div>

        <EG.Card className="content-product-detail">
          <EG.Heading tag="h5">Card title</EG.Heading>
          <div className="flex-wrap">
            <div className="product-date">25/10/2021</div>
            <EG.Button className="add-product-btn">Add to Product</EG.Button>
          </div>
          {/* <EG.Checkbox checked={_selected} onChange={selectCheckBox} /> */}
        </EG.Card>
      </Pane>
    </EG.Card>
  );
};
