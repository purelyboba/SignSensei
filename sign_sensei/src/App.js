import React, { useRef } from 'react';

import Bar from "./components/bar"
import Visualizer from "./components/visualizer";
import Detector from "./components/detector";

function App() {
  return(
    <main>
      <Bar />
      <Visualizer />
      {/* <Detector /> */}
    </main>
  );
}

export default App;
