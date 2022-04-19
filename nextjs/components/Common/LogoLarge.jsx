import _JSXStyle from "styled-jsx/style";

if (typeof global !== "undefined") {
  Object.assign(global, { _JSXStyle });
}

export default () => {
  return (
    <a href="#" className="dropshop-logo normal">
      <img src="/logo.svg" />
    </a>
  );
};
