import React, { useEffect, useState } from "react";
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { heightState, highlightLinkState, highlightNodeState, selectedLinkState, selectedNodeState, toggleDynamicState, toggleSimpleState, widthState } from "../data/recoil-state";
import DynamicGraph from "./DynamicGraph";
import StaticGraph from "./StaticGraph";

const GraphPanel = ({staticData, dynamicData}) => {
  const [colours, setColours] = useState({});
  const [highlightNodes, setHighlightNodes] = useRecoilState(highlightNodeState);
  const [highlightLinks, setHighlightLinks] = useRecoilState(highlightLinkState);
  const [selectedNode, setSelectedNode] = useRecoilState(selectedNodeState);
  const isDynamic = useRecoilValue(toggleDynamicState);
  const isSimpleGraph = useRecoilValue(toggleSimpleState);
  const setWidth = useSetRecoilState(widthState);
  const setHeight = useSetRecoilState(heightState);
  const setSelectedLink = useSetRecoilState(selectedLinkState);

  const updateHighlight = () => {
    setHighlightNodes(highlightNodes);
    setHighlightLinks(highlightLinks);
  };

  const handleNodeClick = (node, data) => {
    highlightNodes.clear();
    highlightLinks.clear();
    setSelectedLink(null);
    
    highlightNodes.add(node);
    data.links.forEach(link => {
      if (link.source.id === node.id) {
        highlightLinks.add(link);
        highlightNodes.add(link.target);
      }
    });
    
    setSelectedNode(node ? {...node} : null);
    updateHighlight();
  };

  const handleLinkClick = (link) => {
    highlightNodes.clear();
    highlightLinks.clear();
    setSelectedNode(null);

    if (link) {
      highlightLinks.add(link);
      highlightNodes.add(link.source);
      highlightNodes.add(link.target);
    }
    
    let newSelected = link ? {...link} : null;
    if (newSelected) {
      newSelected.source = {...newSelected.source};
      newSelected.target = {...newSelected.target};
    }
    setSelectedLink(newSelected);
    updateHighlight();
  };

  useEffect(() => {
    const getRandomInt = (max) => {
      return Math.floor(Math.random() * max);
    };

    const getColor = (classes) => {
      let colourMapping = {};
      let totalColours = (classes.length > 1) ? classes.length : 1;
      let hueSection = 360 / totalColours;

      let h,s,l;
      classes.forEach((c, index) => {
        h = (index * hueSection) + getRandomInt(hueSection * 0.8);
        s = Math.max(getRandomInt(100), 20); 
        s = Math.min(s, 60); 
        l = Math.max(getRandomInt(100), 70); 
        l = Math.min(l, 90); 
        colourMapping[c] = `hsl(${h} ${s}% ${l}%)`;
      });
      
      return colourMapping;
    };

    let classes = [...new Set(staticData.nodes.map(n => n.class))];
    setColours(getColor(classes));
  }, [staticData]);

  useEffect(() => {
    const changeSize = () => {
      setWidth(window.innerWidth * 0.8);
      setHeight(window.innerHeight);
    }
  
    window.addEventListener('resize', changeSize)

    return function cleanup() {
      window.removeEventListener('resize', changeSize);
    };
  });

  const drawNodeHighlight = (node, ctx, bckgDimensions) => {
    let r = isSimpleGraph ? bckgDimensions + 2 : bckgDimensions * 1.05;
    ctx.fillStyle = "gold";
    if (selectedNode && node.id === selectedNode.id) {
      ctx.fillStyle = "rgba(100, 255, 100, 0.8)";
    }
    ctx.beginPath();
    ctx.ellipse(node.x, node.y, r, r, 0, 0, 2 * Math.PI);
    ctx.fill();
  };

  const nodePointerArea = (node, color, ctx) => {
    let simpleSize = Math.max(node.__bckgDimensions / 25, 4);
      const bckgDimensions = isSimpleGraph ? simpleSize : node.__bckgDimensions;
      if (highlightNodes.has(node)) {
        drawNodeHighlight(node, ctx, bckgDimensions);
      }
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.ellipse(node.x, node.y, bckgDimensions, bckgDimensions , 0, 0, 2 * Math.PI);
      ctx.fill();
  }

  const drawText = (node, ctx, text, fontSize) => {
      ctx.lineJoin = 'round';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillStyle = "black";
      ctx.fillText(text, node.x, node.y)

      if (!node.class.endsWith(".py")) {
          ctx.font = `${fontSize * 0.8}px Courier`;
          const classLabel = node.class;
          ctx.fillText(classLabel, node.x, node.y - fontSize);
      }
  };

  return (
    <>
    {!isDynamic && 
      <StaticGraph 
        data={staticData}
        colours={colours}
        handleLinkClick={handleLinkClick}
        handleNodeClick={handleNodeClick}
        drawText={drawText}
        nodePointerArea={nodePointerArea}
      />
    }
    {isDynamic && 
      <DynamicGraph 
        data={dynamicData}
        colours={colours}
        handleLinkClick={handleLinkClick}
        handleNodeClick={handleNodeClick}
        drawText={drawText}
        nodePointerArea={nodePointerArea}
      />}
    </>
  );
}
  
export default GraphPanel;
  