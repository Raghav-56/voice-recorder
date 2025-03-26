document.addEventListener('DOMContentLoaded', function() {
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const recordingsList = document.getElementById('recordingsList');
    const recordingStatus = document.getElementById('recordingStatus');
    const timerDisplay = document.getElementById('timer');
    
    let mediaRecorder;
    let audioChunks = [];
    let startTime;
    let timerInterval;
    
    // Load existing recordings
    loadRecordings();
    
    // Set up event listeners
    recordButton.addEventListener('click', startRecording);
    stopButton.addEventListener('click', stopRecording);
    
    function startRecording() {
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                recordingStatus.textContent = "Recording...";
                recordButton.disabled = true;
                stopButton.disabled = false;
                
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    saveRecording(audioBlob);
                };
                
                // Start timer
                startTime = Date.now();
                timerInterval = setInterval(updateTimer, 1000);
                
                mediaRecorder.start();
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
                recordingStatus.textContent = "Error: Could not access microphone";
            });
    }
    
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            stopButton.disabled = true;
            recordButton.disabled = false;
            recordingStatus.textContent = "Recording stopped";
            
            // Stop timer
            clearInterval(timerInterval);
            timerDisplay.textContent = "00:00";
            
            // Stop all tracks
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    }
    
    function updateTimer() {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
        const seconds = (elapsed % 60).toString().padStart(2, '0');
        timerDisplay.textContent = `${minutes}:${seconds}`;
    }
    
    function saveRecording(audioBlob) {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.wav');
        
        fetch('/save-recording', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                loadRecordings();
            } else {
                console.error('Error saving recording:', data.error);
                recordingStatus.textContent = "Error saving recording";
            }
        })
        .catch(error => {
            console.error('Error:', error);
            recordingStatus.textContent = "Error saving recording";
        });
    }
    
    function loadRecordings() {
        fetch('/recordings')
            .then(response => response.json())
            .then(data => {
                recordingsList.innerHTML = '';
                data.recordings.forEach(filename => {
                    const li = document.createElement('li');
                    
                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = filename;
                    
                    const playButton = document.createElement('button');
                    playButton.textContent = 'Play';
                    playButton.className = 'button';
                    playButton.addEventListener('click', () => {
                        playRecording(filename);
                    });
                    
                    li.appendChild(nameSpan);
                    li.appendChild(playButton);
                    recordingsList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('Error loading recordings:', error);
            });
    }
    
    function playRecording(filename) {
        const audio = new Audio(`/recordings/${filename}`);
        audio.play();
    }
});
