const http = require('http');

// Test the main page
function testMainPage() {
  return new Promise((resolve) => {
    http.get('http://localhost:3000', (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        console.log('Main Page Test:');
        console.log(`- Status Code: ${res.statusCode}`);
        console.log(`- Content Type: ${res.headers['content-type']}`);
        console.log(`- Response Length: ${data.length} bytes`);
        console.log('- Contains expected elements:', 
          data.includes('Our Premium Products') ? '✓' : '✗');
        resolve();
      });
    }).on('error', (e) => {
      console.error('Main Page Test Error:', e.message);
      resolve();
    });
  });
}

// Test product detail page
function testProductDetail() {
  return new Promise((resolve) => {
    http.get('http://localhost:3000/products/1', (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        console.log('\nProduct Detail Test:');
        console.log(`- Status Code: ${res.statusCode}`);
        console.log(`- Content Type: ${res.headers['content-type']}`);
        console.log(`- Response Length: ${data.length} bytes`);
        console.log('- Contains product details:', 
          data.includes('Hedamo Organic Honey') ? '✓' : '✗');
        resolve();
      });
    }).on('error', (e) => {
      console.error('Product Detail Test Error:', e.message);
      resolve();
    });
  });
}

// Run all tests
async function runTests() {
  console.log('Running Application Tests...\n');
  await testMainPage();
  await testProductDetail();
  console.log('\nTests completed.');
}

runTests();
