d3.selectAll('input').data([]).exit().on('mouseenter', (e) => {
    e.target.focus()
})

// let body = document.getElementsByTagName('body')[0]
// document.onresize = () => {
//     console.log(body.clientWidth)
// }