document.addEventListener("DOMContentLoaded", () => {
    const delmodal = document.getElementById("deleteModal");
    const closeBtn = delmodal.querySelector(".close-btn"); // Fix: use delmodal here
    const delmodalFormContainer = document.getElementById("delete-modal-form-container");
    const delLinks = document.querySelectorAll(".delete-link");

    // Handle clicking on the delete link
    delLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const userId = link.getAttribute("data-user-id1");

            // Load the form dynamically via fetch
            fetch(`/delete-user/${userId}/`)
                .then((response) => response.text())
                .then((data) => {
                    delmodalFormContainer.innerHTML = data;
                    delmodal.classList.add("show"); // Show the modal
                })
                .catch((error) => {
                    delmodalFormContainer.innerHTML = "<h2>Error loading form</h2>";
                    console.error("Error:", error);
                });
        });
    });

    // Close modal using close button only
    closeBtn.addEventListener("click", () => {
        delmodal.classList.remove("show"); // Close the modal
    });
});



// for update-profile

  document.addEventListener("DOMContentLoaded", () => {
        const modal = document.getElementById("profileModal");
        const closeBtn = modal.querySelector(".close-btn");
        const modalFormContainer = document.getElementById("modal-form-container");
        const editLinks = document.querySelectorAll(".edit-profile");

        // Handle clicking on the edit link
        editLinks.forEach((link) => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                const userId = link.getAttribute("data-user-id");

                // Load the form dynamically via fetch
                fetch(`/update_profile/${userId}/`)
                    .then((response) => response.text())
                    .then((data) => {
                        modalFormContainer.innerHTML = data;
                        modal.classList.add("show"); // Show the modal
                    })
                    .catch((error) => {
                        modalFormContainer.innerHTML = "<h2>Error loading form</h2>";
                        console.error("Error:", error);
                    });
            });
        });

        // Close modal using close button only
        closeBtn.addEventListener("click", () => {
            console.log('Close button clicked');
            modal.classList.remove("show");
        });
    });



document.addEventListener("DOMContentLoaded", () => {
    const searchInputuser = document.querySelector(".user"); // Input field
    const userTableRows = document.querySelectorAll(".user1 tr"); // Desktop table rows
    const userCards = document.querySelectorAll(".instrument-card"); // Mobile cards

    searchInputuser.addEventListener("input", () => {
        const query = searchInputuser.value.toLowerCase().trim();

        // Search in desktop table
        userTableRows.forEach((row) => {
            const cells = row.querySelectorAll("td");
            const textContent = Array.from(cells)
                .map((cell) => cell.textContent.toLowerCase())
                .join(" ");

            row.style.display = textContent.includes(query) ? "" : "none";
        });

        // Search in mobile cards
        userCards.forEach((card) => {
            const textContent = card.textContent.toLowerCase();
            card.style.display = textContent.includes(query) ? "" : "none";
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const statNumbers = document.querySelectorAll('.stat-card h3');
    
    const animateCount = (element, finalNumber) => {
        const duration = 1800; // 1.8 seconds total
        const startTime = performance.now();
        const easeOutElastic = (t) => {
            return Math.pow(2, -10 * t) * Math.sin((t - 0.075) * (2 * Math.PI) / 0.3) + 1;
        };
        
        const updateNumber = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Elastic ease-out for the first 90%, then smooth finish
            let animationProgress;
            if (progress < 0.9) {
                animationProgress = easeOutElastic(progress / 0.9) * 0.9;
            } else {
                animationProgress = progress; // Linear finish
            }
            
            const currentValue = Math.floor(animationProgress * finalNumber);
            element.textContent = currentValue.toLocaleString();
            
            // Visual feedback - scale slightly during animation
            if (progress < 1) {
                const scale = 1 + (0.1 * Math.sin(progress * Math.PI * 8));
                element.style.transform = `scale(${scale})`;
                requestAnimationFrame(updateNumber);
            } else {
                // Final clean up
                element.textContent = finalNumber.toLocaleString();
                element.style.transform = '';
                
                // Add completion flash
                element.classList.add('count-complete');
                setTimeout(() => element.classList.remove('count-complete'), 600);
            }
        };
        
        // Start animation
        element.textContent = '0';
        requestAnimationFrame(updateNumber);
    };

    // Intersection Observer setup
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const numberElement = entry.target;
                const finalNumber = parseInt(numberElement.textContent);
                animateCount(numberElement, finalNumber);
                observer.unobserve(numberElement);
            }
        });
    }, { threshold: 0.2 });

    // Initialize observer
    statNumbers.forEach(number => {
        number.dataset.originalValue = number.textContent;
        observer.observe(number);
    });
});

