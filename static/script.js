// Handle user registration
document.getElementById('registerForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('User registered successfully!');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Handle user login
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login successful!');
            // Hide login and registration forms and show the survey form
            document.getElementById('registerDiv').style.display = 'none';
            document.getElementById('loginDiv').style.display = 'none';
            document.getElementById('surveyDiv').style.display = 'block';
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Handle survey submission
document.getElementById('submitSurvey').addEventListener('click', function() {
    const paragraph1Choice = document.getElementById('paragraph1').value;
    const paragraph2Choice = document.getElementById('paragraph2').value;

    fetch('http://127.0.0.1:5000/survey', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            paragraph1: paragraph1Choice,
            paragraph2: paragraph2Choice,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Survey submitted successfully!');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
