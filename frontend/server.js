const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Serve the static UI (index.html, css, js) from /public
app.use(express.static(path.join(__dirname, 'public')));

app.listen(PORT, () => {
  console.log(`Frontend running at http://localhost:${PORT}`);
  console.log('Make sure the Flask backend is running at http://localhost:5000');
});