d3.selectAll('input').data([]).exit().on('mouseenter', (e) => {
    e.target.focus()
})