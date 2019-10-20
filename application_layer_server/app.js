var express = require('express');
var app = express();
var path = require('path');
const bodyParser = require('body-parser');
var router = express.Router();
var fs = require('fs')
const _from = "guceconelli@gmail.com"
const email = require('./server.js')
var shell = require('shelljs')

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname+'/index.html'));
  // res.send('Hello World!');
});

app.post('/action_page',function(req, res) {
	res.send("command sent")
	console.log(req.body)

	var user = new email.User("guceconelli@gmail.com");
	user.writeEmail(req.body["to"],req.body["message"]);
    var hasfile = false


})

app.get('/receive_message2', function (req,res) {
  console.log("python: " + req.body.msg);
})

app.post('/receive_message',function(req,res) {
    var msg=req.body.msg;
    console.log("python: " + msg);
    //const path = './../00_physical_layer/physical_layer/server/messages/received/frame.txt'
    //shell.exec(msg)
    res.send(shell.exec(msg))
    res.end();
    console.log('bye')
})


const port = process.env.PORT || 8000;
app.listen(port, function () {
  console.log('Example app listening on port 8000!');
});