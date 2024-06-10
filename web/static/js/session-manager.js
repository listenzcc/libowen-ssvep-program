
/**
 * Fetch the latest sessions and update the #selectSavedDesign.
 * Selecting the options will load the saved design layout
 */
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
            d3.json('getByName?name=' + name).then(data => {
                designTextDom.value = data.content
                clonedDesignTextDom.value = data.content
                redrawCanvas()
            })
        })

    })

}

updateSavedSessions()

// Take over submitting function for formCommitDesignText.
// It commit the current design layout
{
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
}

// Take over Go button
{
    let goBtn = document.getElementById("inputGoButton");


    goBtn.onclick = () => {

        let pkg = Object.assign({}, {
            designText: designTextDom.value,
            resolutionX: document.getElementById("inputMonitorResolutionX").value,
            resolutionY: document.getElementById("inputMonitorResolutionY").value,
            trialBodyLength: document.getElementById('inputTrialBodyLength').value,
            trialHeadLength: document.getElementById("inputTrialHeadLength").value,
            trialTailLength: document.getElementById("inputTrialTailLength").value,
            trialRepeats: document.getElementById("inputTrialRepeats").value,
            cue: document.getElementById('selectCue').value,
            backgroundImageDataUrl: getBackgroundImageDataUrl(),
            patchShape: layoutOptions.selectPatchShape
        });

        console.log(pkg)

        fetch('/go', {
            method: "POST",
            body: new URLSearchParams(pkg) // event.target is the form
        }).then((response) => {
            if (!response.ok) {
                response.json().then((body) => {
                    let msg = [response.status, response.statusText]
                    for (let key in body) {
                        msg.push(`${key}, ${body[key]}`)
                    }
                    alert(msg.join('\n\n'))
                })
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // or response.text() or whatever the server sends
        }).then((body) => {
            // handle body
            console.log(body)
        }).catch((error) => {
            // handle error
            console.error(error)
        });

    }
}