document.addEventListener("DOMContentLoaded", function () {
        const images = document.querySelectorAll(".image-slider img");
        let index = 0;

        function showNextImage() {
            images[index].classList.remove("active");
            index = (index + 1) % images.length;
            images[index].classList.add("active");
        }

        setInterval(showNextImage, 5000); // Change image every 5 seconds
    });



     function showCategory(category, element) {
        // Hide all categories
        document.querySelectorAll('.ins-content > div').forEach(div => {
            div.style.display = 'none';
        });

        // Show the selected category
        document.querySelector(`.${category}`).style.display = 'block';

        // Remove 'active' class from all nav links
        document.querySelectorAll('.nav a').forEach(link => {
            link.classList.remove('active');
        });

        // Add 'active' class to the clicked link
        element.classList.add('active');
    }

    // Automatically show Aerophones on page load
    document.addEventListener("DOMContentLoaded", function () {
        showCategory('Aerophones', document.querySelector('.nav a.active'));
    });