// Check if element exists before adding event listeners
const hoverEle = document.getElementById('stupidJs');

if (hoverEle) {
    function addHoverStyle() {
        hoverEle.style.backgroundColor = 'orange';
        hoverEle.style.color = 'white';
    }

    function removeHoverStyle() {
        hoverEle.style.backgroundColor = 'white';
        hoverEle.style.color = 'black';
    }
    
    hoverEle.addEventListener('mouseenter', addHoverStyle);
    hoverEle.addEventListener('mouseleave', removeHoverStyle);
}

// Track visited review links and add visual indicators
function trackVisitedLinks() {
    const reviewLinks = document.querySelectorAll('.review-card h2 a');
    
    reviewLinks.forEach(link => {
        // Check if this link already has an event listener
        if (link.dataset.hasEventListener === 'true') {
            return; // Skip if already processed
        }
        
        // Check if this link has been visited
        const linkKey = `visited_${link.href}`;
        const hasVisited = localStorage.getItem(linkKey);
        
        if (hasVisited) {
            // Create and add the eye icon
            const eyeIcon = document.createElement('span');
            eyeIcon.className = 'visited-indicator';
            eyeIcon.innerHTML = '👁️ READ';
            eyeIcon.style.cssText = `
                font-size: 0.5em;
                margin-left: 8px;
                opacity: 0.8;
                vertical-align: middle;
                background-color: #8B0000;
                color: white;
                padding: 2px 6px;
                border-radius: 10px;
                font-weight: bold;
                text-decoration: none;
                display: inline-block;
            `;
            
            link.appendChild(eyeIcon);
        }
        
        // Add click event to mark as visited (only once)
        link.addEventListener('click', function() {
            // Only set localStorage if it hasn't been set before
            if (!localStorage.getItem(linkKey)) {
                localStorage.setItem(linkKey, 'true');
            }
        });
        
        // Mark this link as having an event listener
        link.dataset.hasEventListener = 'true';
    });
}

// Add visited link styling to CSS
function addVisitedStyles() {
    const style = document.createElement('style');
    style.textContent = `
        .visited-indicator {
            animation: fadeIn 0.5s ease-in;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 0.8; transform: scale(1); }
        }
    `;
    document.head.appendChild(style);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    addVisitedStyles();
    trackVisitedLinks();
});

// Handle browser back/forward navigation
window.addEventListener('popstate', function() {
    // Only re-run if we're on a page with review links
    if (document.querySelector('.review-card h2 a')) {
        // Small delay to ensure DOM is updated
        setTimeout(() => {
            trackVisitedLinks();
        }, 100);
    }
});

// Also handle when page becomes visible again (for mobile browsers)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden && document.querySelector('.review-card h2 a')) {
        trackVisitedLinks();
    }
});

// Add any other JavaScript functionality here as needed
console.log('Horror Haven JavaScript loaded successfully!');

// Utility functions for managing read stamps
function clearAllReadStamps() {
    // Clear all visited_* items from localStorage
    const keysToRemove = [];
    for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith('visited_')) {
            keysToRemove.push(key);
        }
    }
    keysToRemove.forEach(key => localStorage.removeItem(key));
    
    // Remove all eye icons from the page
    const eyeIcons = document.querySelectorAll('.visited-indicator');
    eyeIcons.forEach(icon => icon.remove());
    
    console.log('All read stamps cleared');
}

function isReviewRead(reviewUrl) {
    const linkKey = `visited_${reviewUrl}`;
    return localStorage.getItem(linkKey) === 'true';
}

// Make utility functions available globally for debugging
window.HorrorHavenUtils = {
    clearAllReadStamps,
    isReviewRead
};