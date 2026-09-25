// Basic JavaScript functionality for the Biometric Voting System

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.createElement('button');
    mobileMenuButton.innerHTML = '☰';
    mobileMenuButton.classList.add('mobile-menu-button');
    document.querySelector('header').appendChild(mobileMenuButton);
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
            }
        });
    });
    
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});

// Form validation function
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            showError(input, 'This field is required');
        } else {
            clearError(input);
        }
    });
    
    return isValid;
}

// Show error message
function showError(input, message) {
    clearError(input);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
    input.style.borderColor = '#e74c3c';
}

// Clear error message
function clearError(input) {
    const errorDiv = input.parentNode.querySelector('.error-message');
    if (errorDiv) {
        errorDiv.remove();
    }
    input.style.borderColor = '#ddd';
}

// Simulate biometric authentication
function simulateBiometricAuth() {
    const authStatus = document.getElementById('auth-status');
    if (authStatus) {
        authStatus.textContent = 'Scanning...';
        authStatus.className = 'scanning';
        
        // Simulate scanning delay
        setTimeout(() => {
            authStatus.textContent = 'Biometric Verification Successful!';
            authStatus.className = 'authenticated';
            
            // Enable vote button after successful authentication
            const voteButton = document.getElementById('vote-button');
            if (voteButton) {
                voteButton.disabled = false;
                voteButton.classList.add('enabled');
            }
        }, 3000);
    }
}

// Call this function to enable the vote button directly
function enableVoteButton() {
    const voteButton = document.getElementById('vote-button');
    if (voteButton) {
        voteButton.disabled = false;
        voteButton.classList.add('enabled');
    }
    
    const authStatus = document.getElementById('auth-status');
    if (authStatus) {
        authStatus.textContent = 'Verification Completed!';
        authStatus.className = 'authenticated';
    }
}