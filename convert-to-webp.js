const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const { exec } = require('child_process');

const execPromise = promisify(exec);

const imagesDir = path.join(__dirname, 'images');

// Get all jpg files
const imageFiles = fs.readdirSync(imagesDir).filter(file => file.endsWith('.jpg'));

console.log(`Found ${imageFiles.length} images to convert`);

async function convertToWebP() {
  for (const file of imageFiles) {
    const inputPath = path.join(imagesDir, file);
    const outputPath = path.join(imagesDir, file.replace('.jpg', '.webp'));

    try {
      // Using ImageMagick convert command (cross-platform)
      const command = `magick "${inputPath}" -quality 85 "${outputPath}"`;
      await execPromise(command);
      console.log(`✓ Converted: ${file} -> ${path.basename(outputPath)}`);

      // Delete original jpg
      fs.unlinkSync(inputPath);
      console.log(`✓ Removed: ${file}`);
    } catch (error) {
      console.error(`✗ Failed to convert ${file}:`, error.message);
    }
  }

  console.log('\nConversion complete!');
}

convertToWebP();
