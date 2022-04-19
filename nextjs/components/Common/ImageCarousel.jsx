import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from "react-responsive-carousel";
import _ from "lodash";

const renderThumbs = (children) => {
  const AddImage = () => (
    <div>
      <img height={70} src="/icons8-add.svg" alt="logo" />
    </div>
  );
  return [<AddImage />, ...children];
};

const _onClickAddImage = ({ i, onClickAddImage }) => {
  if (i == 0) {
    onClickAddImage();
  }
};

const style = {
  image: {
    border: "1px solid #ccc",
    background: "#fefefe",
  },
};

export default ({ dynamicHeight, images, onClickAddImage }) => {
  return (
    <Carousel
      autoPlay
      dynamicHeight={dynamicHeight}
      showThumbs={true}
      onClickThumb={(idx) => _onClickAddImage({ i: idx, onClickAddImage })}
      renderThumbs={renderThumbs}
    >
      {_.map(images, (img_src, idx) => {
        return <img src={img_src} />;
      })}
    </Carousel>
  );
};
