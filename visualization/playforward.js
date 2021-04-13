/* global d3 */

let playerData = []

function makeVisualization() {
  for (let j = 0; j < playerData.length; j += 1) {

    console.log(playerData[j].studentID);
    let singlePlayerData = playerData[j].actions;

    let color = d3.scaleOrdinal()
      .domain([0, 201, 402, 603, 804, 1005])
      .range(['red', 'orange', 'yellow', 'green', 'blue', 'purple']);

    let i = 0;

    d3.select(`#svg${j}`).selectAll('rect').data(singlePlayerData).enter().append('rect')
      .attr('x', 0)
      .attr('y', () => {
        i += 1;
        return (i - 1);
      })
      .attr('width', 40)
      .attr('height', 1)
      .attr('fill', (d) => color(parseInt(d.id)))
      .append('title')
      .text((d) => d.string);

  }
}

d3.text('dataWithActions.txt')
  .then((data) => d3.csvParseRows(data))
  .then((data) => {
    data.forEach(element => {
      element = element.toString();
      let obj = JSON.parse(element);
      if (obj.actions != 'None') {
        playerData.push({studentID: obj.studentID, actions: obj.actions});
      }
    });
    makeVisualization();
  });
