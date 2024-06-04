const fs = require('fs')
const remarkParse = require('remark-parse')
const unified = require('unified')

const formatCategories = require('../../utils/db/format-categories')
const formatJson = require('../../utils/db/format-json')
const formatResources = require('../../utils/db/format-resources')
const groupRowContent = require('../../utils/db/group-row-content')
const separateTables = require('../../utils/db/separate-tables')
const writeToFile = require('../../utils/db/write-to-file')

/**
 * @description Reads and parses a README file, creates lists of resources and
 * categories, writes them to separate JSON files, and throws an error if any issue
 * arises during the process.
 */
async function updateDB() {
    try {
        /**
         * @description Processes input `data`, checking for any errors (`err`) and storing
         * the result (`readme`).
         * 
         * @param { object } err - result of reading the file contents, and it is thrown as
         * an error if there was any issue during the reading process.
         * 
         * @param { object } data - data that is read from the file.
         */
        const readme = fs.readFileSync('./README.md', 'utf-8', (err, data) => {
            if (err) throw err
            readme = data
        })

        const parsedReadme = unified().use(remarkParse).parse(readme).children
        const indexListIndex = parsedReadme.findIndex(child => child.type === 'list')

        // Create resources list
        const separatedTables = separateTables({ readme: parsedReadme, indexListIndex })
        const tablesWithGroupedRowContent = groupRowContent(separatedTables)
        const formattedContent = formatResources(tablesWithGroupedRowContent)

        await writeToFile({
            data: formatJson(formattedContent),
            filePath: './db/resources.json',
        })

        // Create categories list
        const categories = parsedReadme[indexListIndex].children.map(
            category => category.children[0].children[0].children[0].value
        )
        const categoriesList = formatCategories(categories)

        await writeToFile({
            data: formatJson(categoriesList),
            filePath: './db/categories.json',
        })
    } catch (error) {
        throw new Error('Error creating DB files:', error)
    }
}

updateDB()
