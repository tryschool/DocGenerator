const { exec } = require('child_process');
const path = require('path');

const generateDocument = (templatePath, outputPDFPATH, jsonData) => {
    return new Promise((resolve, reject) => {
        // Convert les données json en string escape
        const jsonString = JSON.stringify(jsonData).replace(/"/g, '\\"');

        // Run la cmd pour le script python
        const command = `python3 "${path.join(__dirname, '../../main.py')}" "${templatePath}" "${outputPDFPATH}" "${jsonString}"`;
        
        exec(command, (e, stdout, stderr) => {
            if (e) {
                console.error(`Err : ${stderr}`);
                reject(e);
                return;
            }
            console.log(`OK : ${stdout}`);
            resolve(outputPDFPATH);
        });
    });
};

module.exports = {
    generateDocument
};
