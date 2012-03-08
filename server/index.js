var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {}
handle["/"] = requestHandlers.start;
handle["/lookup"] = requestHandlers.lookup;
handle["/upload"] = requestHandlers.upload;

server.start(router.route, handle);
