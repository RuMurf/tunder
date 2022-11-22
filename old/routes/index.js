var express = require('express');
const multer  = require('multer');
const fs = require('fs');
var router = express.Router();
const shell = require('shelljs');
const mongoose = require('mongoose');

//Connect to MongoDB and initialize schema for song object
mongoose.connect('mongodb://127.0.0.1:27017/tunder');

const songSchema = new mongoose.Schema({
  song_id: Number,
  song_title: String,
  Artist: String,
  Album_id: Number,
  Album_name: String
})

var Song = mongoose.model("songs", songSchema);

//Used to save audio sent from client to be read by song-matching application
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
//API to run song matching application on audio clip provided in request body
router.post("/match", upload.single("audio_data"), function(req,res){
  const spawn = require("child_process").spawn;
  console.log("recieved post request"); //DEBUG
  console.log(req.file.path); //DEBUG
  //Run song matching application passing recieved audio clip as arguement
  const pythonProcess = spawn('C:/Users/Ruairi/Projects/tunder/application/venv/Scripts/python.exe', ["application/src/match_program.py", "sound_files/"+req.file.originalname]);
  pythonProcess.stdout.on("data", function(data) {
    dataToSend = data.toString();
    console.log("data: "+dataToSend)
  });

  //Log python stderr to node.js console for debugging purposes
  pythonProcess.stderr.on('data', err => {
    console.log(String(err));
  });

  pythonProcess.on('close', (code) => {
    //Return match to client
    console.log(dataToSend);
    if (dataToSend == 0) {
      //No match was found
      res.render('result', {song: {song_title: "Inconclusive", Artist: "Sorry, we couldn't find a match.", Album_name: "", Album_id: 0}})
    }
    else {
      //Query database for information about song with ID returned by matching algorithm
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
