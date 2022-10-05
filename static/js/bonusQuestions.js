// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    let filter_item = []
    for (let item of items ) {
        let title = Object.values(item)[0].toLowerCase()
        let filter_text = filterValue.toLowerCase()
        let description = Object.values(item)[1].toLowerCase()

        if (filter_text.includes("!")) {
            if (!title.includes(filter_text.slice(1))) {
                filter_item.push(item)
            }
        }
        else if (filter_text.includes("description:")) {
            if (description.includes(filter_text.slice(12))) {
                filter_item.push(item)
            }
        }
        else if (filter_text.includes("!description")) {
            if (!description.includes(filter_text.slice(13))) {
                        filter_item.push(item)
            }
        }
        else {
            if (title.includes(filter_text) || description.includes(filter_text)) {
                filter_item.push(item)
            }
        }
    }

    return filter_item
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
    console.log("increaseFont")
}

function decreaseFont() {
    console.log("decreaseFont")
}