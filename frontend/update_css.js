const fs = require('fs');

const cssPath = 'src/index.css';
let css = fs.readFileSync(cssPath, 'utf8');

const themeRegex = /@theme\s*{([^}]*)}/g;
let match = themeRegex.exec(css);
if (!match) {
    console.log("No @theme block found");
    process.exit(1);
}

const themeBody = match[1];
const hexRegex = /--(color-([a-zA-Z0-9-]+)):\s*(#[a-zA-Z0-9]{6});/g;
let variables = [];
let hexMatch;

while ((hexMatch = hexRegex.exec(themeBody)) !== null) {
    variables.push({
        fullName: hexMatch[1],
        baseName: hexMatch[2],
        hex: hexMatch[3]
    });
}

let newThemeBody = themeBody;
let rootVars = '';
let darkVars = '';
function invertHex(hex) {
    if (hex.length !== 7) return '#ffffff';
    let r = parseInt(hex.substring(1, 3), 16);
    let g = parseInt(hex.substring(3, 5), 16);
    let b = parseInt(hex.substring(5, 7), 16);

    const isDark = (r * 0.299 + g * 0.587 + b * 0.114) < 128;

    if (isDark) {
        if (r < 30) return "#ffffff";
        if (r < 50) return "#f4f4f5";
        if (r < 80) return "#e4e4e7";
        if (r < 120) return "#d4d4d8";
        return "#a1a1aa";
    } else {
        if (r > 230) return "#18181b";
        if (r > 200) return "#27272a";
        if (r > 150) return "#52525b";
        return "#1e1e1e";
    }
}

variables.forEach(v => {
    newThemeBody = newThemeBody.replace(`--${v.fullName}: ${v.hex};`, `--${v.fullName}: var(--${v.baseName});`);
    rootVars += `  --${v.baseName}: ${invertHex(v.hex)};\n`;
    darkVars += `  --${v.baseName}: ${v.hex};\n`;
});

rootVars = rootVars.replace(/--primary: #.*?;/, '--primary: #2563eb;');

let newCss = css.replace(themeBody, newThemeBody);
const rootInjection = `\n:root {\n${rootVars}}\n`;
const darkInjection = `\n.dark {\n${darkVars}}\n`;

if (newCss.includes(':root {')) {
    newCss = newCss.replace(':root {', rootInjection + '\n:root {');
} else {
    newCss += rootInjection;
}

if (newCss.includes('.dark {')) {
    newCss = newCss.replace('.dark {', darkInjection + '\n.dark {');
} else {
    newCss += darkInjection;
}

fs.writeFileSync(cssPath, newCss, 'utf8');
console.log("CSS Successfully updated for Light/Dark tokens!");
