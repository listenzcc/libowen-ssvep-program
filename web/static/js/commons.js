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

            if (key !== 'eventBuffer') {
                rows.push(`${key}: ${raw[key]}`)
            }
            else if (raw[key] !== '') {
                let ta = document.createElement('textarea')
                Object.assign(ta.style, { 'width': '400px', 'height': '400px' })
                ta.value = raw[key]
                document.getElementById('divExperimentEvents').appendChild(ta)
            }


        }
        statusDiv.innerHTML = ''
        d3.select(statusDiv).selectAll('p').data(rows).enter().append('p').text(d => d)
    }).catch(err => { })
}

setInterval(() => { checkoutDisplayStatus() }, 1000)