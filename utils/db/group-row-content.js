/**
 * @description Maps an array of objects representing tables to new objects with
 * updated properties for each table row, including a name and an expanded list of
 * content items for each row.
 * 
 * @param { object } tables - 2D array of objects, where each object in the array
 * contains the name and rows of a table, which are then transformed into an array
 * of JSON-like objects representing the tables' contents.
 * 
 * @returns { object } an object containing a table with row data.
 */
module.exports = function (tables) {
    /**
     * @description Generates high-quality documentation for given code by creating an
     * array of content items based on the type of each child element in the rows array.
     * 
     * @param { object } name - name of the output document.
     * 
     * @param { array } rows - 2D array of child elements to generate documentation for,
     * with each element representing a table row.
     * 
     * @returns { object } an object containing a `name` property and an `rows` property,
     * where `rows` is an array of objects representing the content of the table.
     */
    return tables.map(({ name, rows }) => {
        const content = []

        rows.forEach((child, i) => {
            if (i === 0) return // Table header

            if (child.type === 'link') {
                content.push({
                    link: child.url,
                    name: child.children[0].value,
                    description: '',
                })
            } else {
                const lastContentItem = content.pop()
                content.push({
                    ...lastContentItem,
                    description: `${lastContentItem.description} ${child.value}`,
                })
            }
        })

        return { name, rows: content }
    })
}
