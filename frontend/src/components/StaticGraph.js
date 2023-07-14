import React, { useEffect, useRef } from "react";
import ForceGraph2D from 'react-force-graph-2d';
import { useRecoilValue } from "recoil";
import { heightState, highlightLinkState, toggleSimpleState, widthState } from "../data/recoil-state";

const StaticGraph = ({data, colours, handleLinkClick, handleNodeClick, drawText, nodePointerArea}) => {
    const width = useRecoilValue(widthState);
    const height = useRecoilValue(heightState);
    const highlightLinks = useRecoilValue(highlightLinkState);
    const isSimpleGraph = useRecoilValue(toggleSimpleState);
    const graphRef = useRef();

    const minLinkLength = 220;
    const defaultNodeSize = 40;

    useEffect(() => {
        graphRef.current.d3Force('link')
        .distance(() => minLinkLength);
        graphRef.current.d3Force("charge")
        .strength(-90);
    }, []);

    const drawNode = (node, ctx) => {
        node.__bckgDimensions = defaultNodeSize; // to re-use in nodePointerAreaPaint
        const text = node.name;
        let area = defaultNodeSize * 0.3;

        const fontSize = area * 10 / (text.length + 1);
        ctx.font = `${fontSize}px Courier`;

        nodePointerArea(node, colours[node.class], ctx);

        if (!isSimpleGraph) {
            drawText(node, ctx, text, fontSize);
        }
    };

    return (
        <ForceGraph2D
            ref={graphRef}
            width={width}
            height={height}
            graphData={data}
            linkDirectionalArrowLength={15}
            linkDirectionalArrowRelPos={1}
            nodeCanvasObject={drawNode}
            linkLineDash={[10, 5]}
            nodePointerAreaPaint={nodePointerArea}
            linkColor={(link) => highlightLinks.has(link) ? "yellow" : "lightyellow"}
            linkWidth={(link) => highlightLinks.has(link) ? 2 : 1}
            autoPauseRedraw={false}
            nodeVal={isSimpleGraph ? null : node => node.__bckgDimensions * 2.5}
            onNodeClick={(node) => handleNodeClick(node, data)}
            onLinkClick={handleLinkClick}
        />
    );
}

export default StaticGraph;
