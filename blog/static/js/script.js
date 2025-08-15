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
        
        // Add click event to mark as visited
        link.addEventListener('click', function() {
            localStorage.setItem(linkKey, 'true');
        });
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
    // Small delay to ensure DOM is updated
    setTimeout(() => {
        trackVisitedLinks();
    }, 100);
});

// Also handle when page becomes visible again (for mobile browsers)
document.addEventListener('visibilitychange', function() {
    if (!document.hidden) {
        trackVisitedLinks();
    }
});

// Add any other JavaScript functionality here as needed
console.log('Horror Haven JavaScript loaded successfully!');