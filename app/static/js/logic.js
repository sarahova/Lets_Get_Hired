// console.log(result)
// var button=d3.select('#submitButton')

// button.on("click", function () {
//     d3.json('/').then(function(result) {
//         console.log(result)
//     })
// })

d3.json('/send').then(function(result) {
    console.log(result)
});