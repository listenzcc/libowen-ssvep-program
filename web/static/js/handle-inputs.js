let inputWatchList,
    canvas = document.getElementById('canvasSSVEPLayout'),
    ctx = canvas.getContext('2d');

inputWatchList = [...document.getElementsByTagName('input')].map((element) => element.getAttribute('id'))

console.log('The inputWatchList is:', inputWatchList)

/**
 * 1 inches = 2.54 cm
 * @param {float} inch 
 * @returns centimeters
 */
function convertInchesToCentimeters(inch) {
    return 2.54 * inch
}

function computePixelsByRadius(pixelsPerCentimeter, degrees, distance) {
    let radius = degrees / 180 * Math.PI
    return pixelsPerCentimeter * Math.tan(radius) * distance
}

function onChanged() {
    let aspectRatio, ctx, pixelsPerCentimeter, options = {}

    inputWatchList.forEach(id => options[id] = document.getElementById(id).value)
    console.log(options)

    aspectRatio = options.inputMonitorResolutionX / options.inputMonitorResolutionY
    canvas.width = canvas.height * aspectRatio

    ctx = canvas.getContext('2d')

    pixelsPerCentimeter = Math.sqrt(canvas.width * canvas.width + canvas.height * canvas.height) / convertInchesToCentimeters(options.inputMonitorSize)

    {
        ctx.fillStyle = '#765765'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
    }

    {
        let cx = options.inputRectCenterX * canvas.width,
            cy = options.inputRectCenterY * canvas.height,
            width = options.inputRectWidth * canvas.width,
            height = options.inputRectHeight * canvas.height;

        ctx.fillStyle = 'white'
        ctx.strokeStyle = 'white'

        // Center
        ctx.beginPath()
        ctx.ellipse(cx, cy, 5, 5, 0, 0, Math.PI * 2)
        ctx.fill()

        // Boundary rect
        ctx.strokeRect(cx - width / 2, cy - height / 2, width, height)

        // 5deg circle
        let r, k = Math.sqrt(2) / 2;
        ctx.font = "12px Arial";
        [5, 10].map(deg => {
            r = computePixelsByRadius(pixelsPerCentimeter, deg, options.inputDistance)
            ctx.beginPath()
            ctx.ellipse(cx, cy, r, r, 0, 0, Math.PI * 2)
            ctx.stroke()
            ctx.fillText(deg + ' deg', cx + 8 + k * r, cy + k * r);
        })

        {
            let scaleX = d3.scaleLinear().domain([0, options.inputPatchesGridColumns]).range([0, width]),
                scaleY = d3.scaleLinear().domain([0, options.inputPatchesGridRows]).range([0, height]),
                offsetX = cx - width / 2 + scaleX(1) / 2,
                offsetY = cy - height / 2 + scaleY(1) / 2,
                x, y;

            for (let i = 0; i < options.inputPatchesGridColumns; i++) {
                for (let j = 0; j < options.inputPatchesGridRows; j++) {
                    x = scaleX(i)
                    y = scaleY(j)
                    ctx.beginPath()
                    ctx.ellipse(x + offsetX, y + offsetY, 2, 2, 0, 0, Math.PI * 2)
                    ctx.fill()
                }
            }

        }
    }


}


// Handle oninput changes for the inputs
inputWatchList.forEach(id => {
    let dom = document.getElementById(id)
    dom.oninput = onChanged
})
onChanged()