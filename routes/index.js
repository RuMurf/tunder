var express = require('express');
const multer  = require('multer');
const fs = require('fs');
var router = express.Router();

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
  res.status(200).send("ok");
  // const pythonProcess = spawn('python',["application/test_output.py"]);
  // pythonProcess.stdout.on("data", function(data) {
  //   console.log(data.toString());
  //   res.write(data);
  //   res.status(200).send("ok");
  // })
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Tunder' });
});


module.exports = router;
