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
        console.log(raw)
        let rows = []
        for (const key in raw) {
            switch (key) {
                case 'passed': {
                    rows.push(`${key}: ${parseFloat(raw[key]).toFixed(2)}`)
                    break
                }

                case 'remain': {
                    rows.push(`${key}: ${parseFloat(raw[key]).toFixed(2)}`)
                    break
                }

                case 'eventBuffer': {
                    // Got event buffer, place it into the textarea and join it to #divExperimentEvents
                    if (raw[key] !== '') {
                        let div = d3.select('#divExperimentEvents').append('div').attr('style', 'max-height: 400px'),
                            ol = div.append('ol').attr('style', 'max-height: 380px; overflow-y: auto');

                        ol.selectAll('li').data(raw[key].split('\n')).enter().append('li').text(d => d)

                        // let ta = document.createElement('textarea')
                        // Object.assign(ta.style, { 'width': '400px', 'height': '400px' })
                        // ta.value = raw[key]
                        // document.getElementById('divExperimentEvents').appendChild(ta)
                    }
                    break
                }

                default: {
                    rows.push(`${key}: ${raw[key]}`)
                }
            }

        }
        statusDiv.innerHTML = ''
        d3.select(statusDiv).selectAll('p').data(rows).enter().append('p').text(d => d)
    }).catch(err => {
        statusDiv.innerHTML = ''
        d3.select(statusDiv).selectAll('p').data(['Display is disconnected!!!']).enter().append('p').text(d => d)

        console.error(err)
    })
}

setInterval(() => { checkoutDisplayStatus() }, 1000)