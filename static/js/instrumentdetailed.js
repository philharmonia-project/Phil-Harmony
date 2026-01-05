// NAVBAR DESIGN
// NAVBAR DESIGN - FIXED VERSION
document.addEventListener('DOMContentLoaded', function() {
    const mobileDetailMenuBtn = document.getElementById('mobile-detail-menu-btn');
    const navbarDetail = document.querySelector('.navbar-detail');
    const headerDetail = document.querySelector('.header-detail-navbar');
    
    // Track if mobile menu is open
    let isMobileMenuOpen = false;
    
    // Mobile menu functionality
    mobileDetailMenuBtn.addEventListener('click', function() {
        const isExpanded = this.getAttribute('aria-expanded') === 'true';
        this.classList.toggle('active');
        navbarDetail.classList.toggle('active');
        this.setAttribute('aria-expanded', !isExpanded);
        
        // Update mobile menu state
        isMobileMenuOpen = !isExpanded;
        
        // Toggle body scroll when menu is open
        document.body.style.overflow = !isExpanded ? 'hidden' : '';
    });
    
    // Close mobile menu when clicking a link
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768 && e.target.closest('.navbar-detail a')) {
            mobileDetailMenuBtn.classList.remove('active');
            navbarDetail.classList.remove('active');
            mobileDetailMenuBtn.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
            isMobileMenuOpen = false;
        }
    });
    
    // Improved scroll behavior
    let lastScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
    let isHidden = false;
    const scrollThreshold = 50;
    const navbarDetailHeight = headerDetail.offsetHeight;
    let scrollTimeout;
    
    function handleScroll() {
        // Don't hide navbar if mobile menu is open
        if (isMobileMenuOpen) {
            return;
        }
        
        const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
        
        if (currentScrollPosition > 10) {
            headerDetail.classList.add('scrolled');
        } else {
            headerDetail.classList.remove('scrolled');
        }
        
        if (Math.abs(currentScrollPosition - lastScrollPosition) > scrollThreshold) {
            if (currentScrollPosition > lastScrollPosition && currentScrollPosition > navbarDetailHeight) {
                if (!isHidden && !navbarDetail.classList.contains('active')) {
                    headerDetail.classList.add('hide');
                    isHidden = true;
                }
            } else {
                if (isHidden) {
                    headerDetail.classList.remove('hide');
                    headerDetail.style.animation = 'none';
                    void headerDetail.offsetWidth;
                    headerDetail.style.animation = 'navbarSlideIn-detail 0.4s cubic-bezier(0.25, 0.8, 0.5, 1)';
                    isHidden = false;
                }
            }
            
            lastScrollPosition = currentScrollPosition;
        }
        
        clearTimeout(scrollTimeout);
        
     
    }
    
    window.addEventListener('scroll', function() {
        requestAnimationFrame(handleScroll);
    });
    
    headerDetail.addEventListener('mouseenter', function() {
        if (isHidden) {
            headerDetail.classList.remove('hide');
            isHidden = false;
            clearTimeout(scrollTimeout);
        }
    });
    
    function handleResize() {
        if (window.innerWidth > 768) {
            mobileDetailMenuBtn.classList.remove('active');
            navbarDetail.classList.remove('active');
            mobileDetailMenuBtn.setAttribute('aria-expanded', 'false');
            document.body.style.overflow = '';
            isMobileMenuOpen = false;
        }
    }
    
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(handleResize, 250);
    });
});
// NAVBAR DESIGN


// BODY DESIGN JS
        // Add smooth scrolling to all links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Show/hide back to top button based on scroll position
        window.addEventListener('scroll', function() {
            const backToTopButton = document.getElementById('backDetailToTop');
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('visible');
            } else {
                backToTopButton.classList.remove('visible');
            }
        });

        // Back to top functionality
        document.getElementById('backDetailToTop').addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const nav = document.querySelector('.simple-nav-detail');
            if (window.scrollY > 50) {
                nav.classList.add('scrolled-nav-detail');
            } else {
                nav.classList.remove('scrolled-nav-detail');
            }
        });

        // Section scroll animation
        function checkScroll() {
            const sections = document.querySelectorAll('.document-detail-section');
            
            sections.forEach(section => {
                const sectionTop = section.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (sectionTop < windowHeight * 0.75) {
                    section.classList.add('visible');
                }
            });
        }

        // Run once on page load
        window.addEventListener('load', checkScroll);
        
        // Run on scroll
        window.addEventListener('scroll', checkScroll);

        // Initialize all sections that are already in view
        document.addEventListener('DOMContentLoaded', function() {
            // Make all sections visible immediately (remove if you prefer the fade-in effect)
            // document.querySelectorAll('.document-detail-section').forEach(section => {
            //     section.classList.add('visible');
            // });
            
            // Or for fade-in effect on page load:
            checkScroll();
        });
// BODY DESIGN JS


// BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY
// BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY // BOOK MODAL FOR INSTRUMENT HISTORY

document.addEventListener('DOMContentLoaded', function() {
    const bookDetailIconContainer = document.getElementById('bookDetailIcon');
    const bookDetailModal = document.getElementById('bookDetailModal');
    const openDetailBookBtn = document.getElementById('openDetailBookBtn');
    const bookDetailContent = document.querySelector('.book-detail-content');
    const pagesDetail = document.querySelectorAll('.page-detail.right-detail');
    const leftDetailPage = document.querySelector('.page-detail.left-detail');
    const closeDetailBookBtn = document.querySelectorAll('.close-detail-book');
    const nextDetailPageBtn = document.querySelectorAll('.next-detail-page');
    const prevDetailPageBtn = document.querySelectorAll('.prev-detail-page');
    let currentDetailPage = 0;
    let isAnimatingDetail = false;

    // Stop pulsing animation after first click
    bookDetailIconContainer.addEventListener('click', function() {
        this.classList.add('clicked');
        bookDetailModal.style.display = 'flex';
    });

    // Open Book Content when clicking "Open Book"
    openDetailBookBtn.addEventListener('click', () => {
        document.querySelector('.book-detail-cover').style.display = 'none';
        bookDetailContent.style.display = 'block';
        showDetailPage(currentDetailPage);
    });

    // Close Book
    closeDetailBookBtn.forEach(btn => {
        btn.addEventListener('click', () => {
            bookDetailModal.style.display = 'none';
            document.querySelector('.book-detail-cover').style.display = 'block';
            bookDetailContent.style.display = 'none';
            currentDetailPage = 0;
            resetDetailPages();
        });
    });

    // Next Page with enhanced animation
    nextDetailPageBtn.forEach(btn => {
        btn.addEventListener('click', () => {
            if (!isAnimatingDetail && currentDetailPage < pagesDetail.length - 1) {
                isAnimatingDetail = true;
                const nextDetailPage = currentDetailPage + 1;
                
                // Update left page content to match current page before flip
                leftDetailPage.innerHTML = pagesDetail[currentDetailPage].innerHTML;
                
                // Add folding effect to page content
                const currentDetailContent = pagesDetail[currentDetailPage].querySelector('.page-detail-content');
                currentDetailContent.classList.add('page-detail-content-folding');
                
                // Set up animation classes
                pagesDetail[currentDetailPage].classList.add('flipping-detail', 'flip-out-detail');
                pagesDetail[nextDetailPage].classList.add('flip-in-detail');
                leftDetailPage.classList.add('flip-in-detail');
                
                // After animation completes
                setTimeout(() => {
                    pagesDetail[currentDetailPage].classList.remove('active-detail', 'flip-out-detail', 'flipping-detail');
                    pagesDetail[nextDetailPage].classList.remove('flip-in-detail');
                    pagesDetail[nextDetailPage].classList.add('active-detail');
                    leftDetailPage.classList.remove('flip-in-detail');
                    currentDetailContent.classList.remove('page-detail-content-folding');
                    
                    currentDetailPage = nextDetailPage;
                    isAnimatingDetail = false;
                }, 700);
            }
        });
    });

    // Previous Page with enhanced animation
    prevDetailPageBtn.forEach(btn => {
        btn.addEventListener('click', () => {
            if (!isAnimatingDetail && currentDetailPage > 0) {
                isAnimatingDetail = true;
                const prevDetailPage = currentDetailPage - 1;
                
                // Update left page content to match previous page before flip
                leftDetailPage.innerHTML = pagesDetail[prevDetailPage].innerHTML;
                
                // Add folding effect to page content
                const currentDetailContent = pagesDetail[currentDetailPage].querySelector('.page-detail-content');
                currentDetailContent.classList.add('page-detail-content-folding');
                
                // Set up animation classes
                pagesDetail[currentDetailPage].classList.add('flipping-detail', 'flip-out-reverse-detail');
                pagesDetail[prevDetailPage].classList.add('flip-in-reverse-detail');
                leftDetailPage.classList.add('flip-in-reverse-detail');
                
                // After animation completes
                setTimeout(() => {
                    pagesDetail[currentDetailPage].classList.remove('active-detail', 'flip-out-reverse-detail', 'flipping-detail');
                    pagesDetail[prevDetailPage].classList.remove('flip-in-reverse-detail');
                    pagesDetail[prevDetailPage].classList.add('active-detail');
                    leftDetailPage.classList.remove('flip-in-reverse-detail');
                    currentDetailContent.classList.remove('page-detail-content-folding');
                    
                    currentDetailPage = prevDetailPage;
                    isAnimatingDetail = false;
                }, 700);
            }
        });
    });

    // Show Current Page
    function showDetailPage(index) {
        pagesDetail.forEach((page, i) => {
            page.classList.remove('active-detail', 'flip-in-detail', 'flip-out-detail', 'flip-in-reverse-detail', 'flip-out-reverse-detail', 'flipping-detail');
            if (i === index) {
                page.classList.add('active-detail');
            }
        });
    }

    // Reset Pages on Close
    function resetDetailPages() {
        pagesDetail.forEach(page => {
            page.classList.remove('active-detail', 'flip-in-detail', 'flip-out-detail', 'flip-in-reverse-detail', 'flip-out-reverse-detail', 'flipping-detail');
        });
        pagesDetail[0].classList.add('active-detail');
    }
});