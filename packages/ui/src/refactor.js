const fs = require('fs');
const path = require('path');

console.log('dir path ' , __dirname)
// Source directory containing your loose component files
// const sourceDir = path.join(__dirname, '..', 'src', 'components', 'ui'); 
const sourceDir = path.join(__dirname, 'components', 'ui');
// ...existing code...
// Target directory where each folder will be created
// const targetDir = path.join(__dirname, '..', 'src', 'components');
const targetDir = path.join(__dirname, 'components' );

if (!fs.existsSync(sourceDir)) {
  console.error('Source directory does not exist:', sourceDir);
//   process.exit(1);
}

fs.readdir(sourceDir, (err, files) => {
  if (err) throw err;

  files.forEach((file) => {
    const srcFilePath = path.join(sourceDir, file);
    const stats = fs.statSync(srcFilePath);

    // Skip directories (only move regular files)
    if (stats.isDirectory()) {
      return;
    }

    // Determine the folder name from the file's base name (before .module or final extension)
    // Example: "Button.module.css" => folderName "Button", "Card.tsx" => folderName "Card"
    const ext = path.extname(file); // e.g. ".tsx", ".css"
    let baseName = path.basename(file, ext); // e.g. "Button.module"
    baseName = baseName.replace(/\.module$/, ''); // remove ".module" if present

    // Create the target folder
    const destFolder = path.join(targetDir, baseName.toLowerCase()); // or keep case if you prefer
    if (!fs.existsSync(destFolder)) {
      fs.mkdirSync(destFolder, { recursive: true });
    }

    // Move the file
    const destFilePath = path.join(destFolder, file);
    fs.renameSync(srcFilePath, destFilePath);

    console.log(`Moved: ${file} -> ${path.relative(targetDir, destFilePath)}`);
  });

  console.log('All files have been reorganized successfully.');
});
