
function updateSavedSessions() {
    let select = d3.select('#selectSavedDesign')

    d3.json('getAll').then(data => {
        console.log(data)
        select.node().innerHTML = ''

        select.selectAll('option')
            .data(data)
            .enter()
            .append('option')
            .text(d => d)
            .attr('value', d => d);

        select.on('change', (e) => {
            let name = e.target.selectedOptions[0].value
            d3.json('get?name=' + name).then(data => {
                designTextDom.value = data.content
                redrawCanvas()
            })
        })

    })

}

updateSavedSessions()

let form = document.getElementById("formCommitDesignText");

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    fetch(event.target.action, {
        method: 'POST',
        body: new URLSearchParams(new FormData(event.target)) // event.target is the form
    }).then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // or response.text() or whatever the server sends
    }).then((body) => {
        // handle body
        console.log(body)
        updateSavedSessions()
    }).catch((error) => {
        // handle error
        console.error(error)
    });
});
