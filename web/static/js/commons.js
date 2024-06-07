{
    d3.selectAll('input').data([]).exit().on('mouseenter', (e) => {
        e.target.focus()
    })
}

{
    let a = document.getElementById('divUserLogin'),
        b = document.getElementById('formUserLogin');

    a.onclick = () => {
        b.style.display = b.style.display === 'none' ? 'block' : 'none'
    }
}

let statusDiv = document.getElementById('divDisplayStatus')

function checkoutDisplayStatus() {
    d3.json('/checkoutDisplayStatus').then(raw => {
        // console.log(raw)
        let rows = []
        for (const key in raw) {
            rows.push(`${key}: ${raw[key]}`)
        }
        statusDiv.innerHTML = ''
        d3.select(statusDiv).selectAll('p').data(rows).enter().append('p').text(d => d)
    }).catch(err => { })
}

setInterval(() => { checkoutDisplayStatus() }, 1000)