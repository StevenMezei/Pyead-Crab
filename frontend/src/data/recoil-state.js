import { atom } from "recoil";

const widthState = atom({
    key: "width",
    default: window.innerWidth * 0.8
});

const heightState = atom({
    key: "height",
    default: window.innerHeight
});

const toggleDynamicState = atom({
  key: "toggleDynamic",
  default: false
});

const toggleSimpleState = atom({
  key: "toggleSimple",
  default: false
});

const highlightNodeState = atom({
  key: "highlightNodes",
  default: new Set()
});

const highlightLinkState = atom({
  key: "highlightLinks",
  default: new Set()
});

const selectedNodeState = atom({
  key: "selectedNode",
  default: null
});

const selectedLinkState = atom({
  key: "selectedLink",
  default: null
});

export {
    widthState,
    heightState,
    toggleDynamicState,
    toggleSimpleState,
    highlightNodeState,
    highlightLinkState,
    selectedNodeState,
    selectedLinkState
};