let inputWatchList,
    options,
    designTextDom = document.getElementById('textareaDesignText'),
    canvas = document.getElementById('canvasSSVEPLayout'),
    ctx = canvas.getContext('2d');

inputWatchList = [...document.getElementsByClassName('watchList')].map((element) => element.getAttribute('id'))

console.log('The inputWatchList is:', inputWatchList)

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
    options = {}
    // Make the options as a dict
    inputWatchList.forEach(id => {
        let dom = document.getElementById(id)
        switch (dom.type) {
            case 'checkbox':
                options[id] = dom.checked
                break;
            default:
                options[id] = dom.value
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


    cx = options.inputMonitorResolutionX * options.inputRectCenterX
    cy = options.inputMonitorResolutionY * options.inputRectCenterY
    width = options.inputMonitorResolutionX * options.inputRectWidth
    height = options.inputMonitorResolutionY * options.inputRectHeight
    offsetX = cx - width / 2
    offsetY = cy - height / 2

    {
        let scaleX = d3.scaleLinear().domain([0, options.inputPatchesGridColumns]).range([0, width]),
            scaleY = d3.scaleLinear().domain([0, options.inputPatchesGridRows]).range([0, height]),
            dx = scaleX(1),
            dy = scaleY(1),
            x, y, omega, phi;

        for (let i = 0; i < options.inputPatchesGridColumns; i++) {
            for (let j = 0; j < options.inputPatchesGridRows; j++) {
                x = parseInt(scaleX(i) + offsetX + dx / 2)
                y = parseInt(scaleY(j) + offsetY + dy / 2)
                w = parseInt(dx * options.inputPatchExtentX)
                h = parseInt(dy * options.inputPatchExtentY)
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
    }

}

/**
 * Parse design from designTextDom
 * @returns The array of the SSVEP patches
 */
function parseDesign() {
    let raw = designTextDom.value,
        split;

    return raw.split(';').map(d => {
        split = d.split(',').map(d => d.trim())
        return Object.assign({}, { pid: split[1], x: split[2], y: split[3], w: split[4], h: split[5] })
    })
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
        aspectRatio = options.inputMonitorResolutionX / options.inputMonitorResolutionY
        canvas.width = canvas.height * aspectRatio

        cx = options.inputRectCenterX * canvas.width
        cy = options.inputRectCenterY * canvas.height
        width = options.inputRectWidth * canvas.width
        height = options.inputRectHeight * canvas.height;

        ctx = canvas.getContext('2d')
        ctx.imageSmoothingEnabled = true;

        // Clear the canvas with background color
        {
            ctx.fillStyle = options.inputScreenColor
            ctx.fillRect(0, 0, canvas.width, canvas.height)
        }
    }

    // Draw overlays
    if (options.inputRulerToggle) {
        ctx.fillStyle = options.inputRulerColor
        ctx.strokeStyle = options.inputRulerColor

        // Center
        ctx.beginPath()
        ctx.ellipse(cx, cy, 5, 5, 0, 0, Math.PI * 2)
        ctx.fill()

        // Boundary rect
        ctx.strokeRect(cx - width / 2, cy - height / 2, width, height)

        // 5deg circle
        let r, k = Math.sqrt(2) / 2;
        ctx.font = "12px Arial";

        pixelsPerCentimeter = Math.sqrt(canvas.width * canvas.width + canvas.height * canvas.height) / convertInchesToCentimeters(options.inputMonitorSize);

        [5, 10].map(deg => {
            r = computePixelsByRadius(pixelsPerCentimeter, deg, options.inputDistance)
            ctx.beginPath()
            ctx.ellipse(cx, cy, r, r, 0, 0, Math.PI * 2)
            ctx.stroke()
            ctx.fillText(deg + ' deg', cx + 8 + k * r, cy + k * r);
        })
    }

    // Draw SSVEP patches
    {
        let design = parseDesign()
        ctx.save()

        ctx.fillStyle = options.inputPatchColor
        ctx.strokeStyle = options.inputPatchColor

        ctx.scale(canvas.width / options.inputMonitorResolutionX, canvas.height / options.inputMonitorResolutionY)

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
inputWatchList.forEach(id => {
    let dom = document.getElementById(id)
    console.log(dom.getAttribute('optionType'))
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
}

generateDesign()
redrawCanvas()