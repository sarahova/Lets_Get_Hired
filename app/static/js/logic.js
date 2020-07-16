// console.log(result)
// var button=d3.select('#submitButton')

// button.on("click", function () {
//     d3.json('/').then(function(result) {
//         console.log(result)
//     })
// })

// d3.json('/send').then(function(result) {
//     console.log(result)
// });


function gifLoad(){
    $("body").append('<div class="scrapeLoad"><img src="/static/img/load.gif"></div>');
  }
  function gifRemove(){
    setTimeout(function(){ $(".scrapeLoad").addClass("hideGif"); }, 3000);
  }

  button.on("click", function () {
    gifLoad()
  })
