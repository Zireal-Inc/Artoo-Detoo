import { readdir, existsSync, mkdirSync, rename } from 'fs';
import { join, extname, basename, dirname } from 'path';
import { fileURLToPath } from 'url';

// Get the directory path
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const directoryPath = join(__dirname);

// Function to move .tsx files into folders with the same name
function moveFiles() {
    readdir(directoryPath, (err, files) => {
        if (err) {
            return console.log('Unable to scan directory: ' + err);
        }

        files.forEach(file => {
            if (extname(file) === '.tsx') {
                const fileNameWithoutExt = basename(file, '.tsx');
                const newDirPath = join(directoryPath, fileNameWithoutExt);

                // Create new directory
                if (!existsSync(newDirPath)) {
                    mkdirSync(newDirPath);
                }

                // Move file to new directory
                const oldPath = join(directoryPath, file);
                const newPath = join(newDirPath, file);

                rename(oldPath, newPath, (err) => {
                    if (err) throw err;
                    console.log(`Moved ${file} to ${newDirPath}`);
                });
            }
        });
    });
}

// Execute the function
moveFiles();
