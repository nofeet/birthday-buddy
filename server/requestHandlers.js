var birthdayDB = require('../fetch_data/birthdays.json');
var querystring = require("querystring");

function lookup(query, response) {
  console.log("Look up birthday in DB");

  var callback = querystring.parse(query)["callback"];

  var year = querystring.parse(query)["year"];
  var month = querystring.parse(query)["month"];
  var day = querystring.parse(query)["day"];
  var key = year + month + day;

  console.log(query.callback);
  try {
    var content = birthdayDB[key];
  } catch (error) {
    response.writeHead(400, {"Content-Type": "text/plain"});
    response.write("Error");
    response.end();
  }

  if (typeof content === "undefined") {
    response.writeHead(200, {"Content-Type": "text/plain"});
    response.write("No Birthday Found");
    response.end();
  }
  response.writeHead(200, {"Content-Type": "text/plain"});
  console.log(callback + "('" + content + "')");
  response.end(callback + "('" + content + "')");
}

function upload(response) {
  console.log("Request handler 'upload' was called.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello Upload");
  response.end();
}

exports.lookup = lookup;
exports.upload = upload;
