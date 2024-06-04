/**
 * @description Returns a JSON object containing the length and entries of an array
 * `entries`.
 * 
 * @param { array } entries - array of objects that contains the data to be serialized
 * into a JSON string by the function.
 * 
 * @returns { object } a JSON object containing the count and entries of the provided
 * `entries` array.
 */
module.exports = function (entries) {
    return `{\n"count": ${entries.length},\n"entries": ${JSON.stringify(entries, null, 4)}}`
}
