let inputSSVEPLayoutWatchList,
    layoutOptions,
    designTextDom = document.getElementById('textareaDesignText'),
    clonedDesignTextDom = document.getElementById('clonedTextareaDesignText'),
    canvas = document.getElementById('canvasSSVEPLayout'),
    ctx = canvas.getContext('2d');

inputSSVEPLayoutWatchList = [...document.getElementsByClassName('SSVEPLayoutWatchList')].map((element) => element.getAttribute('id'))

console.log('The inputWatchList is:', inputSSVEPLayoutWatchList)

/**
 * 1 inches = 2.54 cm
 * @param {float} inch 
 * @returns centimeters
 */
function convertInchesToCentimeters(inch) {
    return 2.54 * inch
}

/**
 * Compute the pixels needed to fit the length of the degrees
 * @param {float} pixelsPerCentimeter 
 * @param {float} degrees 
 * @param {float} distance 
 * @returns pixels
 */
function computePixelsByRadius(pixelsPerCentimeter, degrees, distance) {
    let radius = degrees / 180 * Math.PI
    return pixelsPerCentimeter * Math.tan(radius) * distance
}

function fetchLatestOptions() {
    layoutOptions = {}
    // Make the options as a dict
    inputSSVEPLayoutWatchList.forEach(id => {
        let dom = document.getElementById(id)
        switch (dom.type) {
            case 'checkbox':
                layoutOptions[id] = dom.checked
                break;
            default:
                layoutOptions[id] = dom.value
                break;
        }
    })
}

/**
 * Generate design text based on options
 */
function generateDesign() {
    let cx, cy,
        offsetX, offsetY,
        width, height,
        patches = [];

    fetchLatestOptions()


    cx = layoutOptions.inputMonitorResolutionX * layoutOptions.inputRectCenterX
    cy = layoutOptions.inputMonitorResolutionY * layoutOptions.inputRectCenterY
    width = layoutOptions.inputMonitorResolutionX * layoutOptions.inputRectWidth
    height = layoutOptions.inputMonitorResolutionY * layoutOptions.inputRectHeight
    offsetX = cx - width / 2
    offsetY = cy - height / 2

    {
        let scaleX = d3.scaleLinear().domain([0, layoutOptions.inputPatchesGridColumns]).range([0, width]),
            scaleY = d3.scaleLinear().domain([0, layoutOptions.inputPatchesGridRows]).range([0, height]),
            dx = scaleX(1),
            dy = scaleY(1),
            x, y, omega, phi;

        for (let i = 0; i < layoutOptions.inputPatchesGridColumns; i++) {
            for (let j = 0; j < layoutOptions.inputPatchesGridRows; j++) {
                x = parseInt(scaleX(i) + offsetX + dx / 2)
                y = parseInt(scaleY(j) + offsetY + dy / 2)
                w = parseInt(dx * layoutOptions.inputPatchExtentX)
                h = parseInt(dy * layoutOptions.inputPatchExtentY)
                omega = Math.random() * 10 + 10
                phi = Math.random() * Math.PI * 2
                patches.push(Object.assign({}, { x, y, w, h, omega: omega.toFixed(2), phi: phi.toFixed(2) }))
            }
        }

        patches.map((d, i) => Object.assign(d, { pid: 'p-' + (i + 1) }))
    }

    {
        designTextDom.value = patches.map((d, i) => {
            return [i, d.pid, d.x, d.y, d.w, d.h, d.omega, d.phi].join(',')
        }).join(';\n')
        clonedDesignTextDom.value = designTextDom.value
    }

}

/**
 * Parse design from designTextDom
 * @returns The array of the SSVEP patches
 */
function parseDesign() {
    let raw = designTextDom.value,
        design,
        split;

    design = raw.split(';').map(d => {
        split = d.split(',').map(d => d.trim())
        return Object.assign({}, { pid: split[1], x: split[2], y: split[3], w: split[4], h: split[5] })
    })


    // Check if something is wrong
    {
        // Check if a pid is not unique
        let unique = [...new Set([...design.map(d => d.pid)])]
        if (unique.length < design.length) {
            let msg = unique.map(pid => {
                let n = design.filter(d => d.pid === pid).length
                return n > 1 ? `${pid}: ${n}\n` : ''
            }).filter(d => d)
            alert('Repeat pid is detected.\n' + msg)
        }
    }

    return design
}

function refreshCue(design) {
    let cue = d3.select('#selectCue'),
        optionData = ['!Random', '!NoCue'].concat(design.map(d => d.pid))
    cue.node().innerHTML = ''
    cue.selectAll('option').data(optionData).enter().append('option').text(d => d).attr('value', d => d)
}


/**
 * Redraw the canvas with the latest options
 */
function redrawCanvas() {
    let aspectRatio,
        ctx,
        pixelsPerCentimeter,
        cx, cy, width, height;

    fetchLatestOptions()

    // Re-initialize the canvas and generate ctx
    {
        aspectRatio = layoutOptions.inputMonitorResolutionX / layoutOptions.inputMonitorResolutionY
        canvas.width = canvas.height * aspectRatio

        cx = layoutOptions.inputRectCenterX * canvas.width
        cy = layoutOptions.inputRectCenterY * canvas.height
        width = layoutOptions.inputRectWidth * canvas.width
        height = layoutOptions.inputRectHeight * canvas.height;

        ctx = canvas.getContext('2d')
        ctx.imageSmoothingEnabled = true;

        // Clear the canvas with background color
        {
            ctx.fillStyle = layoutOptions.inputScreenColor
            ctx.fillRect(0, 0, canvas.width, canvas.height)
        }
    }

    // Draw overlays
    if (layoutOptions.inputRulerToggle) {
        ctx.fillStyle = layoutOptions.inputRulerColor
        ctx.strokeStyle = layoutOptions.inputRulerColor

        // Center
        ctx.beginPath()
        ctx.ellipse(cx, cy, 5, 5, 0, 0, Math.PI * 2)
        ctx.fill()

        // Boundary rect
        ctx.strokeRect(cx - width / 2, cy - height / 2, width, height)

        // 5deg circle
        let r, k = Math.sqrt(2) / 2;
        ctx.font = "12px Arial";

        pixelsPerCentimeter = Math.sqrt(canvas.width * canvas.width + canvas.height * canvas.height) / convertInchesToCentimeters(layoutOptions.inputMonitorSize);

        [5, 10].map(deg => {
            r = computePixelsByRadius(pixelsPerCentimeter, deg, layoutOptions.inputDistance)
            ctx.beginPath()
            ctx.ellipse(cx, cy, r, r, 0, 0, Math.PI * 2)
            ctx.stroke()
            ctx.fillText(deg + ' deg', cx + 8 + k * r, cy + k * r);
        })
    }

    // Draw SSVEP patches
    {
        let design = parseDesign()

        refreshCue(design)

        ctx.save()

        ctx.fillStyle = layoutOptions.inputPatchColor
        ctx.strokeStyle = layoutOptions.inputPatchColor

        ctx.scale(canvas.width / layoutOptions.inputMonitorResolutionX, canvas.height / layoutOptions.inputMonitorResolutionY)

        design.map(d => {
            let { pid, x, y, w, h } = d

            ctx.beginPath()
            ctx.ellipse(x, y, 5, 5, 0, 0, Math.PI * 2)
            ctx.fill()

            ctx.strokeRect(x - w / 2, y - h / 2, w, h)
            ctx.font = '' + parseInt(Math.min(w / 4, h / 2)) + "px Arial";
            ctx.fillText(pid, x, y);

        })

        ctx.restore()
    }

}

// Handle oninput changes for the inputs
inputSSVEPLayoutWatchList.forEach(id => {
    let dom = document.getElementById(id)
    switch (dom.getAttribute("optionType")) {
        case 'displayOption':
            dom.oninput = () => {
                redrawCanvas()
            }
            break
        default:
            dom.oninput = () => {
                generateDesign()
                redrawCanvas()
            }
            break

    }
})

// Handle input on #designText
designTextDom.oninput = () => {
    redrawCanvas()
    clonedDesignTextDom.value = designTextDom.value
}

generateDesign()
redrawCanvas()