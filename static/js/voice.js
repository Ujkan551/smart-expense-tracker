function startVoice() {
    const btn = document.getElementById('voiceBtn');
    const status = document.getElementById('voiceStatus');

    // Check if browser supports voice
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
        status.textContent = ' Your browser does not support voice. Use Chrome.';
        return;
    }

    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;

    // Button turns red while listening
    btn.classList.add('listening');
    btn.textContent = '🔴 Listening...';
    status.textContent = 'Speak now — say amount, category and note';

    recognition.start();

    recognition.onresult = function(event) {
        const speech = event.results[0][0].transcript.toLowerCase();
        status.textContent = ' Heard: ' + speech;
        fillForm(speech);
    };

    recognition.onerror = function(event) {
        status.textContent = ' Error: ' + event.error + '. Try again.';
    };

    recognition.onend = function() {
        btn.classList.remove('listening');
        btn.textContent = ' Speak to Add';
    };
}

function fillForm(speech) {
    // Extract amount — looks for any number in speech
    const amountMatch = speech.match(/\d+/);
    if (amountMatch) {
        document.getElementById('amount').value = amountMatch[0];
    }

    // Extract category from speech
    const categories = ['food', 'transport', 'shopping', 'entertainment', 'rent', 'health', 'education', 'other'];
    const categorySelect = document.getElementById('category');
    categories.forEach(cat => {
        if (speech.includes(cat)) {
            categorySelect.value = cat.charAt(0).toUpperCase() + cat.slice(1);
        }
    });

    // Put full speech as note
    document.getElementById('note').value = speech;

    // Auto set today's date
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
}