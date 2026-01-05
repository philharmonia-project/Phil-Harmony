document.addEventListener('DOMContentLoaded', function () {
    const loginModal = document.getElementById("loginModal");
    const loginBtn = document.getElementById("login-btn");
    const loginClose = document.getElementById("loginClose");
    const leftSectionButton = document.getElementById("leftSectionButton");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const loginFormElement = document.getElementById("loginFormElement");
    const registerFormElement = document.getElementById("registerFormElement");

    // Function to show error messages with animation
    function showError(element, message) {
        if (!element || !message) return;
        element.textContent = message;
        element.classList.add('show');
        setTimeout(() => {
            if (element.textContent === message) {
                element.classList.remove('show');
                setTimeout(() => element.textContent = '', 300);
            }
        }, 5000);
    }

    // Function to clear errors
    function clearErrors(form) {
        form.querySelectorAll('.FrontLerror-message').forEach(el => {
            el.classList.remove('show');
            setTimeout(() => el.textContent = '', 300);
        });
    }

    // Function to switch forms with animations
    function switchForms(showForm, hideForm) {
        clearErrors(document.forms[0]);
        hideForm.classList.add("fade-out");
        hideForm.addEventListener("animationend", function onHideAnimationEnd() {
            hideForm.style.display = "none";
            hideForm.classList.remove("fade-out");
            hideForm.removeEventListener("animationend", onHideAnimationEnd);

            showForm.style.display = "block";
            showForm.classList.add("fade-in");
            showForm.addEventListener("animationend", function onShowAnimationEnd() {
                showForm.classList.remove("fade-in");
                showForm.removeEventListener("animationend", onShowAnimationEnd);
                const firstInput = showForm.querySelector('input');
                if (firstInput) firstInput.focus();
            });
        });
    }

    // Show the login modal when login button is clicked
    if (loginBtn) {
        loginBtn.onclick = function () {
            loginModal.style.display = "flex";
            loginForm.style.display = "block";
            registerForm.style.display = "none";
            setTimeout(() => {
                const usernameInput = document.getElementById('login-username');
                if (usernameInput) usernameInput.focus();
            }, 300);
        };
    }

    // Close the modal when close button is clicked
    if (loginClose) {
        loginClose.onclick = function () {
            loginModal.style.display = "none";
        };
    }

    // Close modal when clicking outside content
    loginModal.addEventListener('click', function(e) {
        if (e.target === loginModal) {
            loginModal.style.display = "none";
        }
    });

    // Toggle between Login and Register forms
    if (leftSectionButton) {
        leftSectionButton.addEventListener("click", function () {
            if (loginForm.style.display === "block" || loginForm.style.display === "") {
                switchForms(registerForm, loginForm);
                document.getElementById("leftSectionTitle").textContent = "New Here?";
                document.getElementById("leftSectionText").textContent = "Let the rhythm of our ancestors guide you, discover the soul of the Philippines through its traditional instruments.";
                leftSectionButton.textContent = "Login Now";
            } else {
                switchForms(loginForm, registerForm);
                document.getElementById("leftSectionTitle").textContent = "Welcome Back!";
                document.getElementById("leftSectionText").textContent = "Reconnect with the soulful rhythms of Philippine culture through traditional instruments.";
                leftSectionButton.textContent = "Register Now";
            }
        });
    }

    // Check for errors on page load
    function checkForErrors() {
        const errorMessages = document.querySelectorAll('.FrontLerror-message');
        let hasErrors = false;
        errorMessages.forEach(el => {
            if (el.textContent.trim()) {
                el.classList.add('show');
                hasErrors = true;
                if (!document.querySelector('.error-scrolled')) {
                    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    el.classList.add('error-scrolled');
                }
            }
        });
        return hasErrors;
    }

    if (checkForErrors()) {
        loginModal.style.display = "flex";
        const registerErrors = registerForm.querySelectorAll('.FrontLerror-message');
        const hasRegisterErrors = Array.from(registerErrors).some(el => el.textContent.trim());
        if (hasRegisterErrors) {
            loginForm.style.display = "none";
            registerForm.style.display = "block";
        } else {
            loginForm.style.display = "block";
            registerForm.style.display = "none";
        }
    }

    // Form validation
    function validateFormInputs(form) {
        let isValid = true;
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            const errorId = input.id + '-error';
            const errorElement = document.getElementById(errorId) || document.getElementById(input.id + '-login-error');
            if (!input.value.trim()) {
                showError(errorElement, 'This field is required');
                isValid = false;
            } else if (input.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value)) {
                showError(errorElement, 'Please enter a valid email address');
                isValid = false;
            } else if (input.id === 'password2' && input.value !== document.getElementById('password1').value) {
                showError(errorElement, 'Passwords do not match');
                isValid = false;
            }
        });
        return isValid;
    }

    // Form submit handler
    function handleFormSubmit(form, url, generalErrorId, stayOnPage = false) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const generalErrorElement = document.getElementById(generalErrorId);
            generalErrorElement.textContent = '';
            generalErrorElement.classList.remove('show');
            form.querySelectorAll('.FrontLerror-message').forEach(el => {
                el.textContent = '';
                el.classList.remove('show');
            });

            const submitButton = form.querySelector('button[type="submit"]');
            const originalButtonText = submitButton.textContent;
            submitButton.disabled = true;
            submitButton.textContent = 'Processing...';

            if (!validateFormInputs(form)) {
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
                return;
            }

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (stayOnPage) {
                        // Inline success message for register
                        const successMessage = document.getElementById('registerSuccess');
                        if (successMessage) {
                            successMessage.textContent = data.message || "Registration successful! You can now log in.";
                            successMessage.classList.add('show');
                        } else {
                            alert(data.message || "Registration successful! You can now log in.");
                        }
                        form.reset();
                        switchForms(loginForm, registerForm);
                        document.getElementById("leftSectionTitle").textContent = "Welcome Back!";
                        document.getElementById("leftSectionText").textContent = "Reconnect with the soulful rhythms of Philippine culture through traditional instruments.";
                        leftSectionButton.textContent = "Register Now";
                    } else {
                        window.location.href = data.redirect_url;
                    }
                } else {
                    if (data.error) showError(generalErrorElement, data.error);
                    if (data.errors) {
                        for (const [field, error] of Object.entries(data.errors)) {
                            const errorElement = form.querySelector(`#${field}-error`) || form.querySelector(`#${field}-login-error`);
                            if (errorElement) showError(errorElement, error[0]);
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showError(generalErrorElement, 'An error occurred. Please try again.');
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            });
        });
    }

    // Initialize form handlers
    if (loginFormElement) handleFormSubmit(loginFormElement, '/login/', 'loginError');
    if (registerFormElement) handleFormSubmit(registerFormElement, '/register/', 'registerError', true);

    // Password match check
    const password1 = document.getElementById('password1');
    const password2 = document.getElementById('password2');
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            const errorElement = document.getElementById('password2-error');
            if (password1.value !== password2.value) {
                showError(errorElement, 'Passwords do not match');
            } else {
                errorElement.classList.remove('show');
                setTimeout(() => errorElement.textContent = '', 300);
            }
        });
    }
});




// INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS
// INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS

// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS// INSTRUMENT JS
// INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS // INSTRUMENT JS



// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS
// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS
am4core.ready(function () {
    am4core.useTheme(am4themes_animated);
  
    var chart = am4core.create("chartdiv", am4maps.MapChart);
    chart.geodata = am4geodata_philippinesLow;
    chart.projection = new am4maps.projections.Miller();
  
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    polygonSeries.useGeodata = true;
  
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name}";
    polygonTemplate.fill = am4core.color("#d3d3d3");
    polygonTemplate.stroke = am4core.color("#000000");
    polygonTemplate.strokeWidth = 0.5;
  
    polygonTemplate.events.on("over", function (ev) {
      ev.target.originalFill = ev.target.fill;
      ev.target.fill = am4core.color("#f2d974");
    });
  
    polygonTemplate.events.on("out", function (ev) {
      const hasInstrument = ev.target.dataItem.dataContext.has_instrument;
      ev.target.fill = hasInstrument ? am4core.color("#1E90FF") : am4core.color("#d3d3d3");
    });

    // Function to update the instrument panel
    function updateInstrumentPanel(provinceName, data) {
      const instrumentList = document.getElementById("instrument-list");
      const provinceNameElement = document.getElementById("province-name");
      const provinceDescription = document.getElementById("province-description");
      const noInstruments = document.querySelector(".no-instruments");
      const culturalGroupTag = document.getElementById("cultural-group").querySelector("span");
  
      provinceNameElement.innerText = `Instruments from ${provinceName}`;
      provinceDescription.innerText = `This region is known for the following instruments:`;
  
      // Update cultural group tag
      if (data.length > 0 && data[0].region) {
        culturalGroupTag.textContent = data[0].region;
      } else {
        culturalGroupTag.textContent = "---";
      }
  
      instrumentList.innerHTML = '';
      instrumentList.style.display = 'grid';
      noInstruments.style.display = 'none';
  
      if (data.length === 0) {
        instrumentList.style.display = 'none';
        noInstruments.style.display = 'block';
      } else {
        data.forEach(item => {
          const card = document.createElement('div');
          card.className = 'instrument-card';
          card.innerHTML = `
            <img src="${item.image || 'https://via.placeholder.com/150'}" alt="${item.name}" loading="lazy">
            <p>${item.name}</p>
          `;
          instrumentList.appendChild(card);
        });
      }
    }
  
    // Function to load data for a province
    function loadProvinceData(provinceName) {
      fetch(`/api/instruments/province/?province_name=${provinceName}`)
        .then(response => response.json())
        .then(data => {
          updateInstrumentPanel(provinceName, data);
        });
    }
  
    // Initial load - get provinces with instruments and show the first one
    fetch('/api/instruments/provinces-with-instruments/')
      .then(response => response.json())
      .then(provincesWithInstruments => {
        // Update the map with which provinces have instruments
        polygonSeries.data = polygonSeries.geodata.features.map(feature => {
          const provinceName = feature.properties.name;
          const hasInstrument = provincesWithInstruments.includes(provinceName);
  
          return {
            id: feature.id,
            name: provinceName,
            has_instrument: hasInstrument,
            fill: hasInstrument ? am4core.color("#1E90FF") : am4core.color("#d3d3d3")
          };
        });
        
        // Load data for the first province with instruments
        if (provincesWithInstruments.length > 0) {
          loadProvinceData(provincesWithInstruments[0]);
        }
      });
  
    // Keep the click functionality
    polygonTemplate.events.on("hit", function (ev) {
      const provinceName = ev.target.dataItem.dataContext.name;
      loadProvinceData(provinceName);
    });
  
    // Fix the map position and zoom
    chart.chartContainer.wheelable = false;
    chart.seriesContainer.draggable = false;
    chart.seriesContainer.resizable = false;
    chart.maxZoomLevel = 1;
    chart.minZoomLevel = 1;
    chart.zoomControl = null;
    chart.zoomControl.slider.height = 0;
  
    chart.homeZoomLevel = 1;
    chart.homeGeoPoint = {
      latitude: 12.8797,
      longitude: 121.7740
    };
    chart.goHome();
});
  
  // MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS
  // MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS// MAP JS




//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS
//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS
document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.slider-track');
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.slider-dots .dot');
    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');
    const iconTools = document.querySelectorAll('.icon-tooltip'); // Get all instrument icons
    let currentIndex = 0;
    let autoSlideInterval;
    const slideCount = slides.length;
    
    // Initialize dots
    function initDots() {
        const dotsContainer = document.querySelector('.slider-dots');
        dotsContainer.innerHTML = '';
        
        for (let i = 0; i < slideCount; i++) {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        }
    }
    
    // Update slider position
    function updateSlider() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Update active dot
        document.querySelectorAll('.slider-dots .dot').forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
        
        // Add active class to current slide for animations
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentIndex);
        });

        // Update active icon
        iconTools.forEach((icon, index) => {
            icon.classList.toggle('active', index === currentIndex);
        });
    }
    
    // Go to specific slide
    function goToSlide(index) {
        currentIndex = index;
        updateSlider();
        resetAutoSlide();
    }
    
    // Next slide
    function nextSlide() {
        currentIndex = (currentIndex + 1) % slideCount;
        updateSlider();
        resetAutoSlide();
    }
    
    // Previous slide
    function prevSlide() {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateSlider();
        resetAutoSlide();
    }
    
    // Auto slide
    function startAutoSlide() {
        autoSlideInterval = setInterval(nextSlide, 5000);
    }
    
    // Reset auto slide timer
    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        startAutoSlide();
    }

    // Connect instrument icons to slides
    function connectIconsToSlides() {
        iconTools.forEach((icon, index) => {
            icon.addEventListener('click', () => {
                goToSlide(index);
            });

            // Add hover effect
            icon.addEventListener('mouseenter', () => {
                slides[index].classList.add('highlight');
            });

            icon.addEventListener('mouseleave', () => {
                slides[index].classList.remove('highlight');
            });
        });
    }
    
    // Initialize
    initDots();
    connectIconsToSlides(); // Connect the icons
    startAutoSlide();
    
    // Button controls
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') nextSlide();
        if (e.key === 'ArrowLeft') prevSlide();
    });
    
    // Pause on hover
    const slider = document.querySelector('.image-slider');
    slider.addEventListener('mouseenter', () => clearInterval(autoSlideInterval));
    slider.addEventListener('mouseleave', startAutoSlide);
    
    // Swipe support for touch devices
    let touchStartX = 0;
    let touchEndX = 0;
    
    slider.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        clearInterval(autoSlideInterval);
    }, {passive: true});
    
    slider.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        startAutoSlide();
    }, {passive: true});
    
    function handleSwipe() {
        const threshold = 50;
        if (touchEndX < touchStartX - threshold) {
            nextSlide();
        } else if (touchEndX > touchStartX + threshold) {
            prevSlide();
        }
    }
});
//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS
//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS//HOME PAGE JS


// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS
// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS

// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS
// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS// 3 VIDEO JS

// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS
// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS
document.addEventListener('DOMContentLoaded', function() {
  const scrollElements = document.querySelectorAll('[data-scroll]');
  
  const elementInView = (el, delay = 0) => {
    const elementTop = el.getBoundingClientRect().top;
    const elementOffset = delay * 100; // Adjust based on delay
    return (
      elementTop <= (window.innerHeight * 0.8) + elementOffset
    );
  };
  
  const handleScrollAnimation = () => {
    scrollElements.forEach((el) => {
      const delay = el.getAttribute('data-scroll-delay') || 0;
      if (elementInView(el, delay)) {
        el.classList.add('is-visible');
      }
    });
  };
  
  // Initialize with throttle for performance
  let throttleTimer;
  const throttle = (callback, time) => {
    if (throttleTimer) return;
    throttleTimer = true;
    setTimeout(() => {
      callback();
      throttleTimer = false;
    }, time);
  };
  
  // Set up event listeners
  window.addEventListener('load', () => {
    handleScrollAnimation();
    // Add smooth scroll behavior to the whole page
    document.documentElement.style.scrollBehavior = 'smooth';
  });
  
  window.addEventListener('scroll', () => {
    throttle(handleScrollAnimation, 100);
  });
});
// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS
// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS// MISSION VISSION JS


// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS
// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS

document.addEventListener('DOMContentLoaded', function() {
    // Scroll animation
    const section = document.querySelector('.popular-instruments-section2');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    }, { threshold: 0.1 });
    
    if (section) {
      observer.observe(section);
    }
  
    // Carousel functionality
    const carousel = document.querySelector('.popular-instruments2');
    const prevBtn = document.querySelector('.prev-btn2');
    const nextBtn = document.querySelector('.next-btn2');
    const card = document.querySelector('.instrument-card2');
    
    if (!card) return;
    
    const cardWidth = card.offsetWidth + 24; // card width + gap
    let currentPosition = 0;
    let maxScroll = carousel.scrollWidth - carousel.clientWidth;
    
    function updateButtons() {
        prevBtn.disabled = currentPosition <= 10; // small buffer
        nextBtn.disabled = currentPosition >= maxScroll - 10;
    }
    
    function scrollCarousel(direction) {
        const scrollAmount = Math.min(cardWidth * 3, direction === 'prev' ? currentPosition : maxScroll - currentPosition);
        currentPosition = direction === 'prev' 
            ? Math.max(currentPosition - scrollAmount, 0)
            : Math.min(currentPosition + scrollAmount, maxScroll);
        
        carousel.scrollTo({
            left: currentPosition,
            behavior: 'smooth'
        });
        
        setTimeout(updateButtons, 300);
    }
    
    prevBtn.addEventListener('click', () => scrollCarousel('prev'));
    nextBtn.addEventListener('click', () => scrollCarousel('next'));
    
    // Handle window resize
    function handleResize() {
        maxScroll = carousel.scrollWidth - carousel.clientWidth;
        updateButtons();
    }
    
    // Initialize
    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(carousel);
    updateButtons();
  });

// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS
// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS// POPULAR INSTRUMENT JS


// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN
// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN

  // Carousel functionality
  let currentInstrumentIndex = 0;
  let instruments = Array.from(document.querySelectorAll('.instrument-card1'));
  let totalInstruments = instruments.length;
  let autoRotateInterval;
  
  // Initialize carousel
  function initCarousel() {
    if (totalInstruments === 0) return;
    
    // Reset current index if out of bounds
    if (currentInstrumentIndex >= totalInstruments) {
      currentInstrumentIndex = 0;
    } else if (currentInstrumentIndex < 0) {
      currentInstrumentIndex = totalInstruments - 1;
    }
    
    // Position all cards
    updateCarousel();
    
    // Set active card
    instruments.forEach((card, index) => {
      card.classList.remove('active', 'left-1', 'left-2', 'left-3', 'right-1', 'right-2', 'right-3');
      
      if (index === currentInstrumentIndex) {
        card.classList.add('active');
      } else {
        // Calculate the shortest path difference (considering infinite loop)
        let diff = index - currentInstrumentIndex;
        
        // Handle wrapping for infinite effect
        if (Math.abs(diff) > totalInstruments / 2) {
          diff = diff > 0 ? diff - totalInstruments : diff + totalInstruments;
        }
        
        if (diff < 0) {
          // Left side cards
          const position = Math.min(Math.abs(diff), 3);
          card.classList.add(`left-${position}`);
        } else {
          // Right side cards
          const position = Math.min(diff, 3);
          card.classList.add(`right-${position}`);
        }
      }
    });
  }
  
  // Update carousel position
  function updateCarousel() {
    const container = document.querySelector('.instrument-cards-container1');
    const activeCard = instruments[currentInstrumentIndex];
    
    if (!activeCard) return;
    
    // Center the active card visually
    const cardWidth = activeCard.offsetWidth;
    const containerWidth = container.offsetWidth;
    const offset = (containerWidth / 2) - (activeCard.offsetLeft + (cardWidth / 2));
    container.style.transform = `translateX(${offset}px)`;
  }
  
  // Next instrument
  function nextInstrument() {
    if (totalInstruments === 0) return;
    
    currentInstrumentIndex = (currentInstrumentIndex + 1) % totalInstruments;
    initCarousel();
  }
  
  // Previous instrument
  function prevInstrument() {
    if (totalInstruments === 0) return;
    
    currentInstrumentIndex = (currentInstrumentIndex - 1 + totalInstruments) % totalInstruments;
    initCarousel();
  }
  
  // Filter instruments by category
  function filterInstruments(category) {
    const allCards = document.querySelectorAll('.instrument-card1');
    let hasVisible = false;
    
    allCards.forEach(card => {
      if (category === 'all' || card.dataset.category === category) {
        card.style.display = 'block';
        hasVisible = true;
      } else {
        card.style.display = 'none';
      }
    });
    
    // Update instruments array with only visible cards
    instruments = Array.from(document.querySelectorAll('.instrument-card1[style*="display: block"]'));
    totalInstruments = instruments.length;
    currentInstrumentIndex = totalInstruments > 0 ? 0 : -1;
    
    // Show/hide no results
    document.querySelector('.no-results1').classList.toggle('show', !hasVisible);
    
    if (hasVisible) {
      initCarousel();
    }
    
    // Reset auto-rotate
    resetAutoRotate();
  }
  
  // Set up category button click handlers
  document.querySelectorAll('.category-btn1').forEach(btn => {
    btn.addEventListener('click', function() {
      // Remove .active from all and set on clicked
      document.querySelectorAll('.category-btn1').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      
      const category = this.dataset.category;
      filterInstruments(category);
    });
  });
  
  // View Details button
  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
      const productId = this.dataset.productId;
      // You can implement your view details logic here
      console.log(`View details for product ${productId}`);
      // window.location.href = `/product/${productId}`;
    });
  });
  
  // Auto-rotate functionality
  function startAutoRotate() {
    if (autoRotateInterval) clearInterval(autoRotateInterval);
    autoRotateInterval = setInterval(nextInstrument, 5000);
  }
  
  function resetAutoRotate() {
    if (autoRotateInterval) clearInterval(autoRotateInterval);
    startAutoRotate();
  }
  
  // Initialize carousel on page load
  document.addEventListener('DOMContentLoaded', function() {
    initCarousel();
    startAutoRotate();
    
    // Pause auto-rotate on hover
    document.querySelector('.cards-container-wrapper').addEventListener('mouseenter', () => {
      if (autoRotateInterval) clearInterval(autoRotateInterval);
    });
    
    document.querySelector('.cards-container-wrapper').addEventListener('mouseleave', () => {
      startAutoRotate();
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
      initCarousel();
    });
  });
  
  // Optional: Keyboard navigation
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight') {
      nextInstrument();
    } else if (e.key === 'ArrowLeft') {
      prevInstrument();
    }
  });

  

// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN
// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN// INSTRUMENT WITH DETAILED CAROUSEL DESIGN

// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN
// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN
document.addEventListener('DOMContentLoaded', function() {
    // VIDEO MANAGEMENT SYSTEM
    class VideoManager {
        constructor() {
            this.videos = [];
            this.currentlyPlaying = null;
            this.visibilityObserver = null;
            this.setupVideoManager();
        }

        setupVideoManager() {
            // Initialize all video elements
            this.initVideos();
            
            // Setup intersection observer for visibility
            this.setupVisibilityObserver();
            
            // Setup play/pause event listeners
            this.setupEventListeners();
        }

        initVideos() {
            const videoElements = document.querySelectorAll('video');
            videoElements.forEach(video => {
                const videoObj = {
                    element: video,
                    isPlaying: false,
                    wasPlayingBeforeHidden: false
                };
                
                this.videos.push(videoObj);
                
                // Add data attribute for tracking
                video.dataset.videoId = `video-${this.videos.length}`;
            });
        }

        setupVisibilityObserver() {
            this.visibilityObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const video = entry.target;
                    const videoObj = this.findVideoByElement(video);
                    
                    if (!videoObj) return;
                    
                    if (entry.isIntersecting) {
                        // Video became visible
                        if (videoObj.wasPlayingBeforeHidden && this.currentlyPlaying !== video) {
                            // Only auto-play if no other video is currently playing
                            if (!this.currentlyPlaying) {
                                video.play().catch(e => console.log("Autoplay prevented:", e));
                            }
                        }
                    } else {
                        // Video became invisible
                        if (!video.paused) {
                            videoObj.wasPlayingBeforeHidden = true;
                            video.pause();
                        }
                    }
                });
            }, {
                threshold: 0.3, // At least 30% visible
                rootMargin: '50px' // Add some margin for smoother transitions
            });

            // Observe all videos
            this.videos.forEach(videoObj => {
                this.visibilityObserver.observe(videoObj.element);
            });
        }

        setupEventListeners() {
            this.videos.forEach(videoObj => {
                const video = videoObj.element;
                
                // Play event
                video.addEventListener('play', (e) => {
                    this.handlePlay(e.target);
                });
                
                // Pause event
                video.addEventListener('pause', (e) => {
                    this.handlePause(e.target);
                });
                
                // Click on video toggles play/pause
                video.addEventListener('click', (e) => {
                    this.handleVideoClick(e.target);
                });
                
                // When user interacts with controls
                video.addEventListener('playing', (e) => {
                    this.handlePlay(e.target);
                });
            });
            
            // Pause videos when page becomes hidden (tab switch)
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    this.pauseAllVideos();
                }
            });
            
            // Pause videos when window loses focus
            window.addEventListener('blur', () => {
                this.pauseAllVideos();
            });
        }

        handlePlay(videoElement) {
            // If a different video is already playing, pause it
            if (this.currentlyPlaying && this.currentlyPlaying !== videoElement) {
                this.currentlyPlaying.pause();
                
                // Reset the wasPlaying flag for the paused video
                const previousVideoObj = this.findVideoByElement(this.currentlyPlaying);
                if (previousVideoObj) {
                    previousVideoObj.wasPlayingBeforeHidden = false;
                }
            }
            
            // Set the new currently playing video
            this.currentlyPlaying = videoElement;
            
            // Update video object state
            const videoObj = this.findVideoByElement(videoElement);
            if (videoObj) {
                videoObj.isPlaying = true;
                videoObj.wasPlayingBeforeHidden = false;
            }
        }

        handlePause(videoElement) {
            // If the paused video was the currently playing one, clear it
            if (this.currentlyPlaying === videoElement) {
                this.currentlyPlaying = null;
            }
            
            // Update video object state
            const videoObj = this.findVideoByElement(videoElement);
            if (videoObj) {
                videoObj.isPlaying = false;
            }
        }

        handleVideoClick(videoElement) {
            if (videoElement.paused) {
                videoElement.play();
            } else {
                videoElement.pause();
            }
        }

        findVideoByElement(videoElement) {
            return this.videos.find(v => v.element === videoElement);
        }

        pauseAllVideos() {
            this.videos.forEach(videoObj => {
                if (!videoObj.element.paused) {
                    videoObj.wasPlayingBeforeHidden = true;
                    videoObj.element.pause();
                }
            });
            this.currentlyPlaying = null;
        }

        // Cleanup method (optional)
        destroy() {
            if (this.visibilityObserver) {
                this.videos.forEach(videoObj => {
                    this.visibilityObserver.unobserve(videoObj.element);
                });
                this.visibilityObserver.disconnect();
            }
        }
    }

    // Initialize Video Manager
    const videoManager = new VideoManager();

    // Your existing animation code (keep this)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, index * 150);
            }
        });
    }, { 
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });
    
    const elementsToAnimate = [
        '.header', 
        '.image-description', 
        '.video-section', 
        '.learn-more'
    ];
    
    elementsToAnimate.forEach(selector => {
        document.querySelectorAll(selector).forEach(el => {
            observer.observe(el);
        });
    });
    
    // Smooth scroll for arrow click
    const arrowDown = document.querySelector('.arrow-down');
    if (arrowDown) {
        arrowDown.addEventListener('click', () => {
            const ctaSection = document.querySelector('.cta-section');
            if (ctaSection) {
                ctaSection.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        });
    }
});
// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN
// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN// INSTRUCTOR SECTION DESIGN


// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN
// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN

document.addEventListener('DOMContentLoaded', function() {
    const carousel = document.querySelector('.instrument-carousel');
    const cards = document.querySelectorAll('.instrument-card4:not(.cloned)');
    const prevBtn = document.querySelector('.prev');
    const nextBtn = document.querySelector('.next');
    
    let currentIndex = 0;
    let autoSlideInterval;
    let isAnimating = false;
    const cardWidth = cards[0].offsetWidth + 15; // width + gap
    const visibleCards = Math.floor(carousel.parentElement.offsetWidth / cardWidth);
    
    // Initialize carousel position
    carousel.style.transform = `translateX(0)`;
    
    function updateCarousel(instant = false) {
      if (instant) {
        carousel.style.transition = 'none';
      } else {
        carousel.style.transition = 'transform 0.6s cubic-bezier(0.25, 0.1, 0.25, 1)';
        isAnimating = true;
        setTimeout(() => { isAnimating = false; }, 600);
      }
      carousel.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
    }
    
    function nextSlide() {
      if (isAnimating) return;
      
      currentIndex++;
      updateCarousel();
      
      // When reaching the cloned items, instantly reset to beginning
      if (currentIndex >= cards.length) {
        setTimeout(() => {
          currentIndex = 0;
          updateCarousel(true);
          // Force reflow to make the transition none take effect
          void carousel.offsetWidth;
        }, 600); // Matches the transition duration
      }
    }
    
    function prevSlide() {
      if (isAnimating) return;
      
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      } else {
        // Jump to the end (visual only)
        currentIndex = cards.length;
        updateCarousel(true);
        void carousel.offsetWidth;
        
        setTimeout(() => {
          currentIndex = cards.length - 1;
          updateCarousel();
        }, 10);
      }
    }
    
    // Auto-slide every 3 seconds
    function startAutoSlide() {
      autoSlideInterval = setInterval(() => {
        if (!document.hidden) { // Only slide if tab is active
          nextSlide();
        }
      }, 3000);
    }
    
    // Pause auto-slide on hover
    carousel.addEventListener('mouseenter', () => {
      clearInterval(autoSlideInterval);
    });
    
    // Resume auto-slide when mouse leaves
    carousel.addEventListener('mouseleave', startAutoSlide);
    
    // Pause when tab is inactive
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        clearInterval(autoSlideInterval);
      } else {
        startAutoSlide();
      }
    });
    
    // Manual navigation
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearInterval(autoSlideInterval);
      nextSlide();
      startAutoSlide();
    });
    
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      clearInterval(autoSlideInterval);
      prevSlide();
      startAutoSlide();
    });
    
    // Start the auto-slide
    startAutoSlide();
    
    // Handle responsive adjustments
    window.addEventListener('resize', function() {
      updateCarousel(true);
      void carousel.offsetWidth; // Force reflow
    });
  });

// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN
// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN// SLIDING CAROUSEL DESIGN
