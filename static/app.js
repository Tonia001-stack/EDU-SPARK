// Registration form submission handler
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageElement = document.getElementById('message');

            const response = await fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${password}`
            });
            const data = await response.json();
            messageElement.textContent = data.message;
            if (data.success) {
                messageElement.style.color = 'green';
                // Optional: Redirect to login page after a delay
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000); 
            } else {
                messageElement.style.color = 'red';
            }
        });
    }

    // Login form submission handler
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageElement = document.getElementById('message');
            const submitButton = loginForm.querySelector('button[type="submit"]');
            
            submitButton.textContent = 'Logging in...';
            submitButton.disabled = true;

            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${password}`
            });
            const data = await response.json();
            
            messageElement.textContent = data.message;
            if (data.success) {
                messageElement.style.color = 'green';
                window.location.href = '/premium';
            } else {
                messageElement.style.color = 'red';
            }

            submitButton.textContent = 'Login';
            submitButton.disabled = false;
        });
    }

    // Paystack button handler
    const buyPremiumBtn = document.getElementById('buy-premium-btn');
    if (buyPremiumBtn) {
        buyPremiumBtn.addEventListener('click', async function() {
            const messageElement = document.getElementById('message');
            messageElement.textContent = 'Redirecting to payment...';
            buyPremiumBtn.disabled = true;

            // In a real app, you would get the user's email from the session
            // For this example, we'll use a placeholder email.
            const userEmail = "testuser@example.com";

            try {
                const response = await fetch('/paystack-initiate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `email=${userEmail}`
                });

                const data = await response.json();

                if (data.success) {
                    window.location.href = data.authorization_url;
                } else {
                    messageElement.textContent = `Error: ${data.message}`;
                    buyPremiumBtn.disabled = false;
                }
            } catch (error) {
                messageElement.textContent = `An error occurred: ${error.message}`;
                buyPremiumBtn.disabled = false;
            }
        });
    }
});