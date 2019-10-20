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
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');

app.get('/', function (req, res) {
  res.sendFile(path.join(__dirname+'/index.html'));
  // res.send('Hello World!');
});

app.post('/action_page',function(req, res) {
	res.send("command sent")
  // res.render("response",{page:"seinnao"})
	console.log(req.body)

	var user = new email.User("guceconelli@gmail.com");
	user.writeEmail(req.body["to"],req.body["message"]);
    var hasfile = false
  res.end()

})

app.post('/receive_message',function(req,res) {
    var msg=req.body.msg;
    console.log("application client layer")
    res.render("response",{page:msg})
    // res.setHeader("Content-Type", "text/html");
    // res.write("<p>Hello World</p>");
    // res.send(msg)
    // res.render("response",{page: msg},function (err,html) {
    //   if(err) console.log("err: " + err);
    //   console.log("html: " + html);                        
    //   res.send(html);
    //                 // trying same but forcing status
    //   res.status(200).send(html);
    // });
    res.end()
})


const port = process.env.PORT || 3000;
app.listen(port, function () {
  console.log('Example app listening on port 3000!');
});