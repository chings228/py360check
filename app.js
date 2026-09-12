
const sharp = require('sharp')


/**
 * Extracts a perspective view from an equirectangular image using Sharp.
 * 
 * @param {string} inputPath - Path to input equirectangular image
 * @param {string} outputPath - Path to save extracted image
 * @param {Object} options - Transformation settings
 */
async function extractPerspective(inputPath, outputPath, options = {}) {
    const {
      yaw = 0,         // Horizontal angle (-180 to 180)
      pitch = 0,       // Vertical angle (-90 to 90)
      fov = 90,        // Field of View in degrees
      width = 800,     // Output width
      height = 600      // Output height
    } = options;
  
    // 1. Load source image and obtain raw RGBA pixel buffer + dimensions
    const srcImage = sharp(inputPath);
    const { width: srcWidth, height: srcHeight } = await srcImage.metadata();
    
    const srcBuffer = await srcImage
      .ensureAlpha()
      .raw()
      .toBuffer();
  
    // 2. Allocate output RGBA buffer
    const dstBuffer = Buffer.alloc(width * height * 4);
  
    // Pre-calculate angle conversions to radians
    const yawRad = (yaw * Math.PI) / 180;
    const pitchRad = (pitch * Math.PI) / 180;
    const fovRad = (fov * Math.PI) / 180;
  
    // Focal length calculation
    const f = (0.5 * width) / Math.tan(0.5 * fovRad);
    const cx = width / 2;
    const cy = height / 2;
  
    // Rotation terms
    const cosY = Math.cos(yawRad), sinY = Math.sin(yawRad);
    const cosP = Math.cos(pitchRad), sinP = Math.sin(pitchRad);
  
    // 3. Pixel reprojection loop
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        // Ray vector from camera plane
        const nx = (x - cx) / f;
        const ny = -(y - cy) / f;
        const nz = 1.0;
  
        // Normalize ray length
        const len = Math.sqrt(nx * nx + ny * ny + nz * nz);
        const rx = nx / len;
        const ry = ny / len;
        const rz = nz / len;
  
        // Rotate by Pitch (X-axis) then Yaw (Y-axis)
        const y1 = ry * cosP - rz * sinP;
        const z1 = ry * sinP + rz * cosP;
        const x1 = rx;
  
        const x2 = x1 * cosY + z1 * sinY;
        const y2 = y1;
        const z2 = -x1 * sinY + z1 * cosY;
  
        // Convert 3D vector to spherical coordinates
        const lon = Math.atan2(x2, z2);
        const lat = Math.asin(Math.max(-1, Math.min(1, y2)));
  
        // Map spherical angles to source equirectangular texture coords
        let u = ((lon / Math.PI) + 1) * 0.5 * srcWidth;
        let v = (0.5 - (lat / Math.PI)) * srcHeight;
  
        let srcX = Math.floor(u) % srcWidth;
        if (srcX < 0) srcX += srcWidth;
        let srcY = Math.min(srcHeight - 1, Math.max(0, Math.floor(v)));
  
        // Read source pixel RGBA (4 bytes per pixel)
        const srcIdx = (srcY * srcWidth + srcX) * 4;
        const dstIdx = (y * width + x) * 4;
  
        dstBuffer[dstIdx]     = srcBuffer[srcIdx];     // Red
        dstBuffer[dstIdx + 1] = srcBuffer[srcIdx + 1]; // Green
        dstBuffer[dstIdx + 2] = srcBuffer[srcIdx + 2]; // Blue
        dstBuffer[dstIdx + 3] = srcBuffer[srcIdx + 3]; // Alpha
      }
    }
  
    // 4. Output back to file format (JPEG, PNG, WebP, etc.)
    await sharp(dstBuffer, {
      raw: {
        width,
        height,
        channels: 4
      }
    })
    .jpeg({ quality: 90 })
    .toFile(outputPath);
  
    console.log(`Successfully extracted view to: ${outputPath}`);
  }
  
  // Example Usage:

for (let j=1;j<=2;j++){


  for ( let i=0;i<360; i=i+45){


    extractPerspective(`input${j}_360.jpg`, `output${j}_view-${i}.jpg`, {
      yaw: i,      // Look 45° Right
      pitch: 0,   // Look 15° Down
      fov: 90,      // Field of view
      width: 2048,
      height: 1024
    });
  
  
  }

}
