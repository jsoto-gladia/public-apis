/**
 * @description Maps tables with rows and extracts relevant information from each
 * row, generating a list of objects representing API endpoints and their attributes
 * (description, auth, HTTPS, Cors, link, and category).
 * 
 * @param { array } tables - 2D array of tables that contain information about API
 * endpoints and their associated metadata, which is then transformed into an array
 * of objects for documentation generation.
 * 
 * @returns { object } an array of objects containing metadata about each API entry.
 */
module.exports = function (tables) {
    /**
     * @description Maps through an array of objects and extracts information from each
     * entry's `rawDescription` property to generate a new object with properties `API`,
     * `Description`, `Auth`, `HTTPS`, `Cors`, `Link`, and `Category`.
     * 
     * @param { array } rows - array of objects containing information about different
     * API entries.
     * 
     * @returns { object } an array of objects representing API endpoints with metadata
     * on authentication, HTTPS, CORS, and link to the endpoint.
     */
    return tables
        .map(({ name: categoryName, rows }) => {
            return rows.map(({ link, name: entryName, description: rawDescription }) => {
                const [description, auth, https, cors] = rawDescription
                    .split('|')
                    .map(item => item.trim())
                    .filter(item => item)

                return {
                    API: entryName,
                    Description: description,
                    Auth: auth?.toLowerCase() === 'no' ? '' : auth,
                    HTTPS: https?.toLowerCase() === 'yes' ? true : false,
                    Cors: cors?.toLowerCase(),
                    Link: link,
                    Category: categoryName,
                }
            })
        })
        .flat()
}
