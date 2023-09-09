import React, { useRef,useState } from 'react';
import * as tf from '@tensorflow/tfjs';
import * as handpose from '@tensorflow-models/handpose';
import Webcam from "react-webcam";

import '../App.css';
import { drawHand } from "./util";

function Visualizer() {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  const [coords, setCoords] = useState(new Array(63));

  const runHandpose = async () => {
    const net = await handpose.load()
    console.log('Handpose model loaded.')
    const model = await tf.loadGraphModel('model.json');
    console.log('Predictor model loaded.');
    // loop and detect hands
    setInterval(() => {
      detect(net);
      console.log(coords);
      const tensor = model.predict(tf.tensor(coords, [1, 63]));
      tensor.data().then(data => {
        const predictedClass = data.indexOf(Math.max(...data));
        console.log(`Predicted class: ${predictedClass}`)
      })
    }, 1)
  };

  const detect = async (net) => {
    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null &&
      webcamRef.current.video.readyState === 4
    ) {
      const video = webcamRef.current.video;
      const videoWidth = webcamRef.current.video.videoWidth;
      const videoHeight = webcamRef.current.video.videoHeight;

      webcamRef.current.video.width = videoWidth;
      webcamRef.current.video.height = videoHeight;

      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const hand = await net.estimateHands(video);
      // console.log(hand);

      const ctx = canvasRef.current.getContext("2d");
      drawHand(hand, ctx);

      if (hand["length"] !== 0) {
        const value = hand[0]["landmarks"];
        let revisedValue = new Array(63);
        for (let i = 0; i < 21; i++) {
          revisedValue.push(value[i][0]);
          revisedValue.push(value[i][1]);
          revisedValue.push(value[i][2]);
        }
        setCoords([...revisedValue]);
      }
    }
  }

  runHandpose();

  return (
    <div className='camera_viewer'>
      <Webcam 
        ref={webcamRef}
        style={{
          position: "absolute",
          marginLeft: "auto",
          marginRight: "auto",
          left: 0,
          right: 0,
          textAlign: "center",
          zindex: 9,
          width: 640,
          height: 480
        }} 
      />
      <canvas 
        ref={canvasRef}
        style={{
          position: "absolute",
          marginLeft: "auto",
          marginRight: "auto",
          left: 0,
          right: 0,
          textAlign: "center",
          zindex: 9,
          width: 640,
          height: 480
        }} 
      />
    </div>
  );
}

export default Visualizer;
