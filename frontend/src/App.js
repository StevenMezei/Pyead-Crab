import "./App.css";
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from "react";
import DetailsPanel from "./components/DetailsPanel";
import GraphPanel from "./components/GraphPanel";
import { RecoilRoot } from 'recoil';

function App() {
  const [staticData, setStaticData] = useState({
      nodes: [],
      links: [] 
  });
  const [dynamicData, setDynamicData] = useState({
    nodes: [],
    links: [] 
});

  return (
    <div className="App">
      <div className="content">
        <RecoilRoot>
          <GraphPanel staticData={staticData} dynamicData={dynamicData} />
          <DetailsPanel setStaticData={setStaticData} setDynamicData={setDynamicData} />
        </RecoilRoot>
      </div>
    </div>
  );
}

export default App;
