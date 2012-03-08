var http = require("http");
var url = require("url");

function start(route, handle) {

  function onRequest(request, response) {
    var pathname = url.parse(request.url).pathname;
    var query = url.parse(request.url).query;
    console.log("Request for " + pathname + " received.");

    route(handle, pathname, query, response);
  }

  http.createServer(onRequest).listen(8888);
  console.log("Server has started.");
}

exports.start = start;
