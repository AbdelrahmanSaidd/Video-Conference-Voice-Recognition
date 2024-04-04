window.onload = function() {
    let mediaRecorder;
    let recordingTimer;
    let harker;
    let speakerElement;
    let isSpeaking = false;

    // function to edit the meeting title with the speaker's name
    setTimeout(function() {
        speakerElement = document.querySelector('.ouH3xe');
        if (speakerElement) {
            speakerElement.textContent = 'Speaker: ';
        } else {
            console.error('Speaker element not found.');
        }
    }, 3000);
    

    //recording function
    function startRecording(stream) {
        if (!stream) {
            console.error('No microphone stream available.');
            return;
        }

        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = function(e) {
            const reader = new FileReader();
            reader.onloadend = function() {
                const base64data = reader.result;
                const formData = new FormData();
                formData.append('audio', base64data);

                fetch('http://localhost:8000', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(text => {
                    console.log('Server response text:', text);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            };
            reader.readAsDataURL(e.data);
        };

        // Start recording
        mediaRecorder.start();

        // Stop recording to send
        recordingTimer = setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
        }, 3000);

        // Start recording the next chunk when the current one ends
        mediaRecorder.onstop = function() {
            clearTimeout(recordingTimer);
            if (isSpeaking) { 
                // Only start a new recording if voice activity is detected
                startRecording(stream);
            }
        };
    }

    // Check for microphone access and start recording
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            harker = hark(stream);
            harker.on('speaking', function() {
            console.log('Voice activity detected, starting recording...');
            
            speakerElement = document.querySelector('.ouH3xe');
            if (speakerElement) {
                speakerElement.textContent = 'Speaker: Joe';
            } else {
                console.error('Speaker element not found.');
            }
                
                isSpeaking = true; 
                startRecording(stream);
            });

            harker.on('stopped_speaking', function() {
                console.log('Voice activity stopped.');

                speakerElement = document.querySelector('.ouH3xe');
                if (speakerElement) {
                    speakerElement.textContent = 'Speaker:';
                } else {
                    console.error('Speaker element not found.');
                }

                isSpeaking = false; 
                mediaRecorder.stop();
                clearTimeout(recordingTimer);
            });
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
};