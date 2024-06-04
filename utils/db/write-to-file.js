const fs = require('fs')

/**
 * @description Writes data to a file using `fs.writeFile()` and handles potential
 * errors by throwing an error message if any occur.
 * 
 * @param { object } data - data that will be written to the specified file path.
 * 
 * @param { string } filePath - file path where the data will be written.
 * 
 * @returns { undefined } a void value.
 * 
 * 		- `data`: The input data passed to the function.
 * 		- `filePath`: The file path where the data was written.
 */
module.exports = async function ({ data, filePath }) {
    await fs.writeFile(filePath, data, error => {
        if (error) {
            throw new Error(`Error writing to file: ${error}`)
        }
    })

    return
}
