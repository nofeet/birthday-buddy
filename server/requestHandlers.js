var birthdayDB = require('../fetch_data/birthdays.json');
var querystring = require("querystring");

function lookup(query, response) {
  console.log("Look up birthday in DB");

  var year = querystring.parse(query)["year"];
  var month = querystring.parse(query)["month"];
  var day = querystring.parse(query)["day"];
  var key = year + month + day;
  var content = birthdayDB[key];

  response.writeHead(200, {"Content-Type": "text/html"});
  response.write(content);
  response.end();
}

function upload(response) {
  console.log("Request handler 'upload' was called.");
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.write("Hello Upload");
  response.end();
}

exports.lookup = lookup;
exports.upload = upload;
