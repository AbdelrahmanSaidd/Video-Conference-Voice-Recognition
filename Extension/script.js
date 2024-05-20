window.onload = function() {
    let mediaRecorder;
    let recordingTimer;
    // let harker;
    let speakerElement;
    // let isSpeaking = false;
    // let silenceTimer;
    let flag= false;

    // Create a new element to display the speaker's name
    speakerElement = document.createElement('div');
    speakerElement.id = 'speakerElement';
    speakerElement.textContent = 'Speaker: ';
    speakerElement.style.fontSize = '25px';
    document.body.appendChild(speakerElement);


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

                fetch('http://localhost:50000', {
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
                    if (text === 'Speaker Not Detected') {
                        // Server indicates no speaker detected, prompt user for name
                        const speakerName = prompt('Speaker not detected. Please enter your name:');
                        if (speakerName) {
                            // Send entered name back to server in next request
                            formData.append('speakerName', speakerName);
                            speakerElement.textContent = 'Speaker:'; // Clear speaker display
                        }
                    } 
                    else if(text === 'Silence'){
                        speakerElement.textContent = 'Speaker:'; // Clear speaker display
                    }
                    else if(text.startsWith('Is')){
                        const userResponse = confirm(text);
                        if(userResponse){
                            const userResponse2 = confirm("Please introduce yourself in 10 seconds after confirming");
                            if(userResponse2){
                                mediaRecorder.stop;
                                flag= true;
                            }
                        }
                        else{
                            const speakerName = prompt('Speaker not detected. Please enter your name:');
                            if (speakerName) {
                                // Send entered name back to server in next request
                                formData.append('speakerName', speakerName);
                                speakerElement.textContent = 'Speaker:'; // Clear speaker display
                            }
                        }
                    }
                    else {
                        console.log('Speaker identified:', text);
                        speakerElement.textContent = `Speaker: ${text}`;
                    }
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
            if(flag==true){
                startRecording2(stream);
            }
            else{
                startRecording(stream);
            }
            // if (isSpeaking) { 
                // Only start a new recording if voice activity is detected
            // }
            // else{
            //     silenceTimer = setTimeout(function() {
            //         speakerElement.textContent = 'Speaker: ';
            //     },2000); // Replace 2000 with desired silence detection time in milliseconds
            // }
        };
    }

    //recording function
    function startRecording2(stream) {
        if (!stream) {
            console.error('No microphone stream available.');
            return;
        }

        mediaRecorder = new MediaRecorder(stream);

        // Start recording
        mediaRecorder.start();

        // Stop recording to send
        recordingTimer = setTimeout(() => {
            if (mediaRecorder && mediaRecorder.state === 'recording') {
                mediaRecorder.stop();
            }
        }, 10000);

        // Start recording the next chunk when the current one ends
        mediaRecorder.onstop = function() {
            clearTimeout(recordingTimer);
            // if (isSpeaking) { 
                // Only start a new recording if voice activity is detected
                flag==false;
                startRecording(stream);
            // }
            // else{
            //     silenceTimer = setTimeout(function() {
            //         speakerElement.textContent = 'Speaker: ';
            //     },2000); // Replace 2000 with desired silence detection time in milliseconds
            // }
        };
    }

    // Check for microphone access and start recording
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            // harker = hark(stream);
            // harker.on('speaking', function() {
            // console.log('Voice activity detected, starting recording...');
                    
            // isSpeaking = true; 
            // clearTimeout(silenceTimer);
            if(flag==true){
                startRecording2(stream);
            }
            else{
                startRecording(stream);
            }
            // });

            // harker.on('stopped_speaking', function() {
            //     console.log('Voice activity stopped.');

            //     isSpeaking = false; 
            //     mediaRecorder.stop();
            //     clearTimeout(recordingTimer);

            //     speakerElement.textContent = 'Speaker:';
            // });
        })
        .catch(error => {
            console.error('Error accessing microphone:', error);
        });
};
