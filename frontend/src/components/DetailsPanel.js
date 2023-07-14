import React from "react";
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
import { useRecoilState, useRecoilValue, useSetRecoilState } from "recoil";
import { highlightLinkState, selectedLinkState, selectedNodeState, toggleDynamicState, toggleSimpleState } from "../data/recoil-state";

const DetailsPanel = ({setStaticData, setDynamicData}) => {
  const logo = require("../data/pyeadCrab2.png");
  const selectedNode = useRecoilValue(selectedNodeState);
  const selectedLink = useRecoilValue(selectedLinkState);
  const selectedLinks = useRecoilValue(highlightLinkState);
  const [isDynamic, setIsDynamic] = useRecoilState(toggleDynamicState);
  const setIsSimple = useSetRecoilState(toggleSimpleState);

  const onToggleDynamic = (e) => {
    setIsDynamic(e.target.checked);
  };

  const onToggleSimple = (e) => {
    setIsSimple(e.target.checked);
  };

  const handleUpdateClick = () => {
    delete require.cache[require.resolve("../data/static.json")];
    delete require.cache[require.resolve("../data/dynamic.json")];
    const staticData = require("../data/static.json");
    const dynamicData = require("../data/dynamic.json");

    setStaticData(staticData);
    setDynamicData(dynamicData);
  }

  const getCallees = () => {
    return <ul>{[...selectedLinks].map((link, i) => <li key={i}>{link.target.id}</li>)}</ul>;
  };

  return (
    <div className="details-panel">
      <div id="logo" >
        <img id="pyeadCrab" src={logo} width="50vw" alt="logo" />
        <h1>pyeadCrab</h1>
      </div>
      <br />
      <hr />
      <Form>
        <div className="loader" >
          <Button 
            variant="primary"
            onClick={handleUpdateClick}
          >
            Update
          </Button>
        </div>
        <Form.Switch 
          type="switch"
          id="dynamic-graph-switch"
          label="Show Dynamic Graph"
          onChange={onToggleDynamic}
        />
        <Form.Switch 
          type="switch"
          id="simple-graph-switch"
          label="Show Simplified Graph"
          onChange={onToggleSimple}
        />
      </Form>
      <hr />
      {selectedNode && 
        <p>
          Function: {selectedNode.name} <br/>
          Class: {selectedNode.class} <br/>
          {isDynamic && <>Called: {selectedNode.calls ? selectedNode.calls + " times" : ""} <br/></>} 
          Calls: <br/>
          {getCallees()}
        </p>
      }
      {selectedLink && 
      <p>
        Link: <br/>
        Caller: {selectedLink.source.name} <br/>
        Callee: {selectedLink.target.name} <br/>
    </p>}
    </div>
  );
}

export default DetailsPanel;
  