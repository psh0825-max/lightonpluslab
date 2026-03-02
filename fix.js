const fs = require('fs');
let c = fs.readFileSync('index.html', 'utf8');
// Remove the guide link div from bible-explorer card
c = c.replace(/<div style="margin-top:10px;"><a href="https:\/\/bible-explorer[^"]*\/guide"[^>]*>[^<]*<\/a><\/div>/g, '');
fs.writeFileSync('index.html', c, 'utf8');
console.log('done');
