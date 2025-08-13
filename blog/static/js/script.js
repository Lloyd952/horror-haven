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

// Add any other JavaScript functionality here as needed
console.log('Horror Haven JavaScript loaded successfully!');