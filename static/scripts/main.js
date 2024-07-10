document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById("predictButton");
    const textarea = document.getElementById("codeSnippet");

    console.log("Button:", button);
    console.log("Textarea:", textarea);

    if (button && textarea) {
        // Function to update button visibility based on textarea content
        function updateButtonVisibility() {
            if (textarea.value.trim() === '') {
                button.style.display = 'none';
            } else {
                button.style.display = 'block';
            }
        }

        // Add input event listener to textarea
        textarea.addEventListener('input', updateButtonVisibility);

        // Initial check on page load
        updateButtonVisibility();
    } else {
        console.error("Button or textarea not found in the DOM.");
    }
});
