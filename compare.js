const cv = require('@techstark/opencv-js');

const { createCanvas, loadImage } = require('canvas');

async function isSubImageInside(mainPath, subPath, threshold = 0.8) {
  const [mainImg, subImg] = await Promise.all([
    loadImage(mainPath),
    loadImage(subPath)
  ]);

  // Convert loaded images to OpenCV matrices
  const src = imageToMat(mainImg);
  const templ = imageToMat(subImg);
  const result = new cv.Mat();

  // Perform template matching
  cv.matchTemplate(src, templ, result, cv.TM_CCOEFF_NORMED);

  // Retrieve match score and coordinates
  const minMax = cv.minMaxLoc(result);
  const confidence = minMax.maxVal; // Value between 0.0 and 1.0

  // Free WebAssembly memory
  src.delete();
  templ.delete();
  result.delete();

  return {
    found: confidence >= threshold,
    confidence: confidence,
    location: minMax.maxLoc
  };
}

function imageToMat(img) {
  const canvas = createCanvas(img.width, img.height);
  const ctx = canvas.getContext('2d');
  ctx.drawImage(img, 0, 0);
  const imgData = ctx.getImageData(0, 0, img.width, img.height);
  return cv.matFromImageData(imgData);
}

// Usage Example




isSubImageInside('./output_view-0.png', './output_view-120', 0.85)
  .then((res) => {
    if (res.found) {
      console.log(`Image found at X: ${res.location.x}, Y: ${res.location.y}`);
      console.log(`Match confidence: ${(res.confidence * 100).toFixed(1)}%`);
    } else {
      console.log('Image not found.');
    }
  });