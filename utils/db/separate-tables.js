/**
 * @description Filters and maps child elements within a Readme file to extract named
 * tables.
 * 
 * @param { array } readme - document containing the markdown syntax that will be
 * transformed into a JSON array of tables.
 * 
 * @param { integer } indexListIndex - index of the first row to be extracted from
 * the Markdown file.
 * 
 * @returns { object } an array of objects containing `name` and `rows` properties,
 * where `name` is the name of a heading and `rows` is an array of rows corresponding
 * to that heading.
 */
module.exports = function ({ readme, indexListIndex }) {
    /**
     * @description Generates a tuple of `name` and `rows` based on the properties of a
     * child element within a React component tree.
     * 
     * @param { node/nodes. } child - child element of the current level of the JSON tree
     * being traversed.
     * 
     * 		- `i`: The current index of the child element in the `indexList`.
     * 		- `child`: The input provided, which is an object with various attributes and properties.
     * 		- `type`: The type of the `child` element, which can be either `'heading'` or
     * another value.
     * 		- `depth`: The depth of the `child` element in the Markdown tree, which can be
     * either 3 or another value.
     * 		- `children`: An array of child elements, each with their own properties and attributes.
     * 
     * 	The function then returns an object containing the `name` property of the
     * `child.children[0]` element and the `rows` property of the `readme[i + 1].children`.
     * 
     * @param { integer } i - 0-based index of a document in the `readme` array.
     * 
     * @returns { object } an object with two properties: `name` and `rows`.
     */
    return readme
        .map((child, i) => {
            if (i <= indexListIndex) return

            if (child.type === 'heading' && child.depth === 3) {
                const name = child.children[0].value
                const rows = readme[i + 1].children

                return { name, rows }
            }
        })
        .filter(table => table)
}
