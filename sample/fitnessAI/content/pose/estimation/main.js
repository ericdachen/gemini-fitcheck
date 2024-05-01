// let capture;
// let posenet;
// let noseX,noseY;
// let reyeX,reyeY;
// let leyeX,leyeY;
// let singlePose,skeleton;
// let actor_img;
// let specs,smoke;
// let video;
// let button;

// function setup() {  // this function runs only once while running
//     createCanvas(2400, 1500);
//     // video = createVideo(['videos/2024.04.11_GYM_ADAM.mp4'])
//     //console.log("setup funct");
//     capture = createCapture(VIDEO);
//     capture.hide();
//     // video.hide()

//     //load the PoseNet model
//     posenet = ml5.poseNet(capture, modelLOADED);
//     // posenet = ml5.poseNet(video, modelLOADED);
//     //detect pose
//     posenet.on('pose', recievedPoses);

//     // Create a button for playing / pausing the video
//     // button = createButton('Play/Pause');
//     // button.position(19, 19);
//     // button.mousePressed(toggleVideo); // Function to be called when the button is clicked 



//     // actor_img = loadImage('images/shahrukh.png');
//     // specs = loadImage('images/spects.png');
//     // smoke = loadImage('images/cigar.png');
// }

// // function toggleVideo() {
// //     if (!video.elt.paused) {
// //         video.pause();
// //     } else {
// //         video.loop();
// //         video.volume(0); // Mute the video
// //     }
// // }

// function recievedPoses(poses) {
//     console.log(poses);

//     if(poses.length > 0) {
//         singlePose = poses[0].pose;
//         skeleton = poses[0].skeleton;
//     }
// }

// function modelLOADED() {
//     console.log("model has loaded");
// }

// /*
// function getRandomArbitrary(min, max) { // generate random num
//     return Math.random() * (max - min) + min;
// }
// */
// function draw() { // this function code runs in infinite loop
    
//     // images and video(webcam)
//     image(capture, 0, 0);
//     // image(video, 0, 0);
//     fill(255, 0, 0);
    
//     if(singlePose) {
//         console.log('hi')
//         for(let i=0; i<singlePose.keypoints.length; i++) {
//             ellipse(singlePose.keypoints[i].position.x, singlePose.keypoints[i].position.y, 10, 10);
//         }

//         stroke(255, 255, 255);
//         strokeWeight(5);

//         for(let j=0; j<skeleton.length; j++) {
//             line(skeleton[j][0].position.x, skeleton[j][0].position.y, skeleton[j][1].position.x, skeleton[j][1].position.y);
//         }

//     }
    
// }

// ml5.js: Pose Estimation with PoseNet
// The Coding Train / Daniel Shiffman
// https://thecodingtrain.com/Courses/ml5-beginners-guide/7.1-posenet.html
// https://youtu.be/OIo-DIOkNVg
// https://editor.p5js.org/codingtrain/sketches/ULA97pJXR

let video;
let poseNet;
let pose;
let singlePose;
let skeleton;
let button;
let frameCount;

function setup() {
  createCanvas(2400, 1500);
//   video = createCapture(VIDEO);
  video = createVideo(['videos/2024.04.11_GYM_ERIC.mp4'])
  video.hide();

  poseNet = ml5.poseNet(video, modelLoaded);
  poseNet.on('pose', gotPoses);

    button = createButton('Play/Pause');
    button.position(19, 19);
    button.mousePressed(toggleVideo); // Function to be called when the button is clicked 

}

function gotPoses(poses) {
  //console.log(poses); 
  if (poses.length > 0) {
    singlePose = poses[0].pose;
    skeleton = poses[0].skeleton;
  }
}

function toggleVideo() {
    if (!video.elt.paused) {
        video.pause();
    } else {
        video.loop();
        video.volume(0); // Mute the video
    }
}


function modelLoaded() {
  console.log('poseNet ready');
}

// Define body connections
const connections = [
    ['leftShoulder', 'leftElbow'], ['leftElbow', 'leftWrist'],
    ['rightShoulder', 'rightElbow'], ['rightElbow', 'rightWrist'],
    ['leftShoulder', 'rightShoulder'],
    ['leftHip', 'rightHip'],
    ['leftShoulder', 'leftHip'], ['rightShoulder', 'rightHip'],
    ['leftHip', 'leftKnee'], ['leftKnee', 'leftAnkle'],
    ['rightHip', 'rightKnee'], ['rightKnee', 'rightAnkle']
];

function drawConnection(partA, partB, color) {
    let pointA = singlePose.keypoints.find(k => k.part === partA);
    let pointB = singlePose.keypoints.find(k => k.part === partB);
    if (pointA && pointB && pointA.score > 0.2 && pointB.score > 0.2) {
        stroke(color);
        strokeWeight(5);
        line(pointA.position.x, pointA.position.y, pointB.position.x, pointB.position.y);
    }
}

function drawPart(partName, color, size) {
    let part = singlePose.keypoints.find(k => k.part === partName && k.score > 0.5); // k.score higher means drawing less and more important points
    if (part && part.score > 0.2) {
        fill(color);
        noStroke();
        ellipse(part.position.x, part.position.y, size, size);
    }
}

function draw() {
    background(255); // Clear the canvas with a white background
    image(video, 0, 0); // Display the video

    if (singlePose) {
        // Draw all keypoints
        drawPart('nose', 'red', 16, 16);
        drawPart('leftEye', 'green', 16, 16);
        drawPart('rightEye', 'green', 16, 16);
        drawPart('leftEar', 'blue', 16, 16);
        drawPart('rightEar', 'blue', 16, 16);
        drawPart('leftShoulder', 'yellow', 16, 16);
        drawPart('rightShoulder', 'yellow', 16, 16);
        drawPart('leftElbow', 'purple', 16, 16);
        drawPart('rightElbow', 'purple', 16, 16);
        drawPart('leftWrist', 'orange', 16, 16);
        drawPart('rightWrist', 'orange', 16, 16);
        drawPart('leftHip', 'pink', 16, 16);
        drawPart('rightHip', 'pink', 16, 16);
        drawPart('leftKnee', 'cyan', 16, 16);
        drawPart('rightKnee', 'cyan', 16, 16);
        drawPart('leftAnkle', 'magenta', 16, 16);
        drawPart('rightAnkle', 'magenta', 16, 16);

        // Draw connections
        connections.forEach(conn => {
            drawConnection(conn[0], conn[1], 'grey');
        });
        saveCanvas('frame' + frameCount, 'jpg');
    }
}
