/**
 * @description Maps the `categories` array to an array of objects with `name` and
 * `slug` properties, where each object represents a category with a unique slug
 * constructed from its name using a set pattern.
 * 
 * @param { array } categories - array of categories to which the returned objects'
 * `name` and `slug` properties will correspond.
 * 
 * @returns { object } an array of objects containing the `name` and `slug` properties
 * of each `category`.
 */
module.exports = function (categories) {
    return categories.map(category => ({
        name: category,
        slug: category
            .trim()
            .toLowerCase()
            .replace(/&/g, 'and')
            .replace(/[^A-Z0-9/]+/gi, '-')
            .replace(/\s/g, '-'),
    }))
}
