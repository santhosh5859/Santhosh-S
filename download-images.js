const fs = require('fs');
const https = require('https');
const path = require('path');

// Create images directory if it doesn't exist
const imagesDir = path.join(__dirname, 'public', 'images');
if (!fs.existsSync(imagesDir)) {
  fs.mkdirSync(imagesDir, { recursive: true });
}

// Product images to download
const images = [
  { name: 'honey.jpg', url: 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=800&auto=format&fit=crop&q=80' },
  { name: 'shea-butter.jpg', url: 'https://images.unsplash.com/photo-1600857544200-b2f666a6e7f5?w=800&auto=format&fit=crop&q=80' },
  { name: 'argan-oil.jpg', url: 'https://images.unsplash.com/photo-1601001815894-4cd6f68a1db0?w=800&auto=format&fit=crop&q=80' }
];

// Function to download an image
function downloadImage(image) {
  return new Promise((resolve, reject) => {
    const filePath = path.join(imagesDir, image.name);
    const file = fs.createWriteStream(filePath);
    
    https.get(image.url, (response) => {
      response.pipe(file);
      
      file.on('finish', () => {
        file.close();
        console.log(`Downloaded ${image.name}`);
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filePath, () => {}); // Delete the file if there's an error
      console.error(`Error downloading ${image.name}:`, err.message);
      reject(err);
    });
  });
}

// Download all images
async function downloadAllImages() {
  try {
    console.log('Starting image downloads...');
    for (const image of images) {
      await downloadImage(image);
    }
    console.log('All images downloaded successfully!');
  } catch (error) {
    console.error('Error downloading images:', error);
  }
}

// Run the download
downloadAllImages();
