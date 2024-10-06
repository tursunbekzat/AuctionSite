document.addEventListener('DOMContentLoaded', function () {
    // Elements for statistics
    const stats = [
        {
            elementId: 'active-auctions',
            targetValue: 5000,
            duration: 100000
        },
        {
            elementId: 'registered-users',
            targetValue: 10000,
            duration: 100000
        },
        {
            elementId: 'total-sales',
            targetValue: 1000000,
            duration: 100000
        }
    ];

    // Function to animate a value from 0 to targetValue
    function animateValue(element, startValue, targetValue, duration) {
        let startTime = null;
        
        function animationStep(currentTime) {
            if (!startTime) {
                startTime = currentTime;
            }
            const progress = Math.min((currentTime - startTime) / duration, 1);
            const currentValue = Math.floor(progress * (targetValue - startValue) + startValue);
            element.textContent = currentValue.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animationStep);
            }
        }

        requestAnimationFrame(animationStep);
    }

    // Trigger animation for each stat
    stats.forEach(stat => {
        const element = document.getElementById(stat.elementId);
        if (element) {
            animateValue(element, 0, stat.targetValue, stat.duration);
        }
    });
});