$( document ).ready(function() {
    let rec = null;
    let audioStream = null;
    let recordTime = 1000*30

    const recordButton = document.getElementById("recordButton");

    recordButton.addEventListener("click", startRecording);

    function startRecording() {

        let constraints = { audio: true, video:false }

        recordButton.disabled = true;

        navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
            const audioContext = new window.AudioContext();
            audioStream = stream;
            const input = audioContext.createMediaStreamSource(stream);
            rec = new Recorder(input, { numChannels: 1 })
            rec.record()
            document.getElementById("output").innerHTML = "Listening..."
        }).catch(function(err) {
            recordButton.disabled = false;
        });

        setTimeout(stopRecording, recordTime);
    }

    function stopRecording() {
        recordButton.disabled = false;
        rec.stop();
        audioStream.getAudioTracks()[0].stop();
        rec.exportWAV(uploadSoundData);
    }

    function uploadSoundData(blob) {
        const filename = "sound-file-" + new Date().getTime() + ".wav";
        const formData = new FormData();
        formData.append("audio_data", blob, filename);
        
        fetch('/match', {
            method: 'POST',
            body: formData
        }).then(async result => { 
            document.getElementById("output").innerHTML = await result.text();
        }).catch(error => { 
            document.getElementById("output").innerHTML = "An error occurred: " + error;
        })
    }
});