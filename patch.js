const fs = require('fs');

function patchFile(filepath) {
  let html = fs.readFileSync(filepath, 'utf8');
  if (!html.includes('const resolveImg')) {
    html = html.replace('<script>', '<script>\n  const resolveImg = (p) => p ? (p.startsWith(\'http\') ? p : \'/\' + p) : \'\';');
    html = html.replace(/src="\/\$\{([^}]+)\}\?t=/g, 'src="${resolveImg($1)}?t=');
    fs.writeFileSync(filepath, html);
    console.log('Patched ' + filepath);
  } else {
    console.log('Already patched ' + filepath);
  }
}

patchFile('admin/dashboard.html');
// index.html and blog.html don't use src="/${...}" they use src="${...}" so they are fine, but let's check
let indexHtml = fs.readFileSync('index.html', 'utf8');
console.log('indexHtml has /${ ? ', indexHtml.includes('src="/${'));
