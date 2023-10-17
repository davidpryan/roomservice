const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

// Specify the path to the folder containing the images
const folderPath = './images';

// Check if the folder exists
if (!folderExists(folderPath)) {
  console.log(`The folder '${folderPath}' does not exist.`);
  process.exit(1);
}

// Read the list of image files in the folder
const imageFiles = getImageFiles(folderPath);

// Initialize a p5-like sketch
function sketch(p) {
  let currentImageIndex = 0;

  p.setup = () => {
    const canvas = createCanvas(800, 600);
    p.createCanvas(800, 600);
    p.noLoop();
    p.loadNextImage();
  };

  p.draw = () => {
    // Display the current image
    const img = p.loadImage(folderPath + '/' + imageFiles[currentImageIndex]);
    p.image(img, 0, 0, p.width, p.height);
  };

  p.keyPressed = () => {
    if (p.keyCode === p.RIGHT) {
      currentImageIndex = (currentImageIndex + 1) % imageFiles.length;
      p.redraw();
    } else if (p.keyCode === p.LEFT) {
      currentImageIndex = (currentImageIndex - 1 + imageFiles.length) % imageFiles.length;
      p.redraw();
    }
  };
}

// Initialize p5-like sketch
const canvasSketch = require('canvas-sketch');
const settings = {
  p5: sketch,
};

canvasSketch(settings);

function folderExists(path) {
  return fs.existsSync(path);
}

function getImageFiles(path) {
  const fs = require('fs');
  return fs.readdirSync(path).filter(file => /\.(png|jpg|jpeg|gif|bmp)$/i.test(file));
}
