document.addEventListener('DOMContentLoaded', function() {
    const materialSelect = document.querySelector('select[name="material"]');
    const wireSizeSelect = document.querySelector('select[name="wire_size"]');

    // 1. Dynamic Wire Size Dropdown
    // This updates the options based on your conductors.json logic
    const wireOptions = {
        "Copper": ["30mm2", "50mm2", "80mm2", "100mm2", "125mm2", "150mm2", "200mm2", "250mm2"],
        "Aluminum": ["80mm2", "125mm2", "150mm2", "250mm2"]
    };

    materialSelect.addEventListener('change', function() {
        const selectedMaterial = this.value;
        const options = wireOptions[selectedMaterial];

        // Clear existing options
        wireSizeSelect.innerHTML = '';

        // Add new options
        options.forEach(size => {
            const opt = document.createElement('option');
            opt.value = size;
            opt.textContent = size + (size === "125mm2" ? " (250MCM)" : "");
            wireSizeSelect.appendChild(opt);
        });
    });

    // 2. Visual Feedback for %VD
    // If you add an ID to your input, we can warn the student in real-time
    const vdInput = document.querySelector('input[name="desired_vd"]');
    vdInput.addEventListener('input', function() {
        if (this.value > 5) {
            this.style.borderColor = 'orange';
            console.log("Warning: Recommended limit is usually 5% or less.");
        } else {
            this.style.borderColor = '#ced4da';
        }
    });
});

// 3. Optional: Function to animate the steps in solution.html
function revealSteps() {
    const steps = document.querySelectorAll('.step-card');
    steps.forEach((step, index) => {
        setTimeout(() => {
            step.style.opacity = '1';
            step.style.transform = 'translateY(0)';
        }, index * 500); // 0.5 second delay between steps
    });
}