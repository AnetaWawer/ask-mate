// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)
    console.log(typeof(items))


    if (sortDirection === "asc") {
            items.sort((a,b) => {
                return (a[sortField] < b[sortField] ? -1 : 1)
            })
    }
    else {
        items.sort((a,b) => {
                return (a[sortField] > b[sortField] ? -1 : 1)
        })
    }
    return items
}

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

function increaseFont(fontSize) {
    var computedFontSize = window.getComputedStyle(document.getElementsByTagName("body")[0]).fontSize;
    let strFontSize = computedFontSize.slice(0,2)
    let intFontSize = parseInt(strFontSize)
    intFontSize += 5
    if (intFontSize <= 30){
        strFontSize = intFontSize.toString()
    document.getElementsByTagName("table")[0].style.fontSize = strFontSize + "px";
    document.getElementsByTagName("body")[0].style.fontSize = strFontSize + "px";}
}

function decreaseFont() {
    var computedFontSize = window.getComputedStyle(document.getElementsByTagName("body")[0]).fontSize;
    let strFontSize = computedFontSize.slice(0,2)
    let intFontSize = parseInt(strFontSize)
    intFontSize -= 5
    if (intFontSize >= 3){
        strFontSize = intFontSize.toString()
    document.getElementsByTagName("table")[0].style.fontSize = strFontSize + "px";
    document.getElementsByTagName("body")[0].style.fontSize = strFontSize + "px";}
}