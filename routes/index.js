var express = require('express');
const multer  = require('multer');
const fs = require('fs');
var router = express.Router();
const shell = require('shelljs');
const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1:27017/tunder-songs');

const songSchema = new mongoose.Schema({
  song_id: Number,
  song_title: String,
  Artist: String,
  Album_id: Number,
  Album_name: Number
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
  //res.status(200).send("ok");

  const pythonProcess = spawn('C:/Users/Ruairi/Projects/tunder/application/venv/Scripts/python.exe', ["application/src/match_program.py", "audio/R1-Invaders.wav"]);
  pythonProcess.stdout.on("data", function(data) {
    console.log("datatosend: "+data.toString());
    dataToSend = data.toString().slice(0, -1);
  });

  pythonProcess.stderr.on('data', err => {
    console.log(String(err));
  });

  pythonProcess.on('close', (code) => {
    console.log('child process close all stdio with code ${code}');
    //send data to browser
    console.log(dataToSend);
    if (dataToSend == 0) {
      res.send(0);
    }
    else {
      var song = Song.findOne({"song_id": parseInt(dataToSend)}, function(err, song) {
        res.send(song)
      });
    }
  });
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Tunder' });
});


module.exports = router;
