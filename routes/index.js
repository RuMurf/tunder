var express = require('express');
const multer  = require('multer');
const fs = require('fs');
var router = express.Router();
const shell = require('shelljs');
const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1:27017/tunder');

const songSchema = new mongoose.Schema({
  song_id: Number,
  song_title: String,
  Artist: String,
  Album_id: Number,
  Album_name: String
})

var Song = mongoose.model("songs", songSchema);

const storage = multer.diskStorage(
  {
      destination: './sound_files/',
      filename: function (req, file, cb ) {
          cb( null, file.originalname);
      }
  }
);

const upload = multer( { storage: storage } );
router.use(express.static('./'));
router.post("/match", upload.single("audio_data"), function(req,res){
  const spawn = require("child_process").spawn;
  console.log("recieved post request");
  console.log(req.file.path);
  const pythonProcess = spawn('C:/Users/Ruairi/Projects/tunder/application/venv/Scripts/python.exe', ["application/src/match_program.py", "sound_files/"+req.file.originalname]);
  pythonProcess.stdout.on("data", function(data) {
    dataToSend = data.toString();
    console.log("data: "+dataToSend)
  });

  pythonProcess.stderr.on('data', err => {
    console.log(String(err));
  });

  pythonProcess.on('close', (code) => {
    //send data to browser
    console.log(dataToSend);
    if (dataToSend == 0) {
      res.render('result', {song: {song_title: "Inconclusive", Artist: "Sorry, we couldn't find a match.", Album_name: "", Album_id: 0}})
    }
    else {
      Song.findOne({"song_id": parseInt(dataToSend)}, function(err, song) {
        if(err){
          console.log(String(err))
        }
        console.log(song)
        res.render('result', {song: song})
      });
    }
  });
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Tunder' });
});


module.exports = router;
