const fs = require('fs');
const path = require('path');

const componentsDir = path.join(__dirname, '.');

const getComponentNames = (filePath) => {
    const content = fs.readFileSync(filePath, 'utf-8');
    const exportRegex = /export\s+{([^}]+)}/g;
    const matches = [...content.matchAll(exportRegex)];
    return matches.flatMap((match) =>
        match[1].split(',').map((name) => name.trim())
    );
};

const generateIndexFile = () => {
    const folders = fs
        .readdirSync(componentsDir)
        .filter((file) =>
            fs.statSync(path.join(componentsDir, file)).isDirectory()
        );
    let imports = [];
    let exports = [];

    folders.forEach((folder) => {
        const tsxFile = path.join(componentsDir, folder, `${folder}.tsx`);
        if (fs.existsSync(tsxFile)) {
            const componentNames = getComponentNames(tsxFile);
            imports.push(
                `import { ${componentNames.join(', ')} } from './${folder}/${folder}';`
            );
            exports.push(...componentNames);
        }
    });

    const indexContent = `${imports.join('\n')}\n\nexport {\n  ${exports.join(
        ',\n  '
    )}\n};\n`;

    fs.writeFileSync(path.join(componentsDir, 'index.tsx'), indexContent);
};

generateIndexFile();
