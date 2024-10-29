const documentService = require('../services/document.service');
const path = require('path');
const fs = require('fs');

const generateDocument = async (req, res) => {
    try {
        const templatePath = req.file.path; // Path du fichier odt
        const data = JSON.parse(req.body.data); // Convert les data json en obj js
        
        // Path de l'ouput du pdf gen
        const outputPDFPATH = path.join(__dirname, '../../output', `${Date.now()}_output.pdf`);
        
        // Service pour run le script python by Elie 
        await documentService.generateDocument(templatePath, outputPDFPATH, data);

        // Envoi du PDF
        res.setHeader('Content-Disposition', 'attachment; filename=generated_document.pdf');
        res.setHeader('Content-Type', 'application/pdf');
        res.sendFile(outputPDFPATH, (err) => {
            // Suppr les fichiers tempo après l'envoi
            fs.unlinkSync(templatePath);
            fs.unlinkSync(outputPDFPATH);
        });
    } catch (error) {
        console.error("Err :", error);
        res.status(500).send({ error: 'Erreur lors de la génération du document' });
    }
};

module.exports = {
    generateDocument
};
