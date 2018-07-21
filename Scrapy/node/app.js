var express = require('express');
var app = express();
var TAC = require('./_signatureTAC')
// console.log(TAC.sign.x.toString())
console.log(TAC.sign.x.toString())
console.log(TAC.sign.toString())

app.get('/', function(req, res){
  res.send('API');
});




app.get('/toutiao/signature/:uid', function(req, res){
     if (req.params.uid) {
       var text = req.params.uid + '' + '0'
       var signature = TAC.sign(text)
       res.send(signature)
     } else {
       res.send('Need a param  of UID')
     }
});



app.listen(3000)