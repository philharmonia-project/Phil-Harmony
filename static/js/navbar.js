// Enhanced JavaScript with navbar hide/show on scroll
function confirmLogout() {
  return confirm("Are you sure you want to logout?");
}

// Toggle Sidebar
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebar-toggle');
const closeSidebar = document.getElementById('close-sidebar');
const navOverlay = document.getElementById('nav-overlay');
const body = document.body;
const navbar = document.querySelector('.header-navbar');
const navbarHeight = navbar.offsetHeight;

let lastScrollPosition = 0;

function openSidebar() {
  sidebar.classList.add('active');
  navOverlay.classList.add('active');
  body.classList.add('sidebar-open');
}

function closeSidebarFunc() {
  sidebar.classList.remove('active');
  navOverlay.classList.remove('active');
  body.classList.remove('sidebar-open');
}

sidebarToggle.addEventListener('click', openSidebar);
closeSidebar.addEventListener('click', closeSidebarFunc);
navOverlay.addEventListener('click', closeSidebarFunc);

// Mobile Menu Toggle
function toggleMenu() {
  const navbarMenu = document.querySelector('.navbar');
  navbarMenu.classList.toggle('active');
  navOverlay.classList.toggle('active');
}

document.getElementById('mobile-menu-icon').addEventListener('click', toggleMenu);

// Dropdown functionality
document.querySelectorAll(".dropdown").forEach((dropdown) => {
  dropdown.addEventListener("mouseenter", () => {
      const content = dropdown.querySelector(".dropdown-content");
      content.style.display = "block";
      setTimeout(() => {
          content.style.opacity = "1";
          content.style.visibility = "visible";
      }, 10);
  });

  dropdown.addEventListener("mouseleave", () => {
      const content = dropdown.querySelector(".dropdown-content");
      content.style.opacity = "0";
      content.style.visibility = "hidden";
      setTimeout(() => {
          content.style.display = "none";
      }, 300);
  });
});

// Close dropdowns when clicking outside (for mobile)
document.addEventListener('click', function(event) {
  if (!event.target.closest('.dropdown') && window.innerWidth <= 992) {
      document.querySelectorAll('.dropdown-content').forEach(content => {
          content.style.opacity = "0";
          content.style.visibility = "hidden";
          setTimeout(() => {
              content.style.display = "none";
          }, 300);
      });
  }
});

// Scroll behavior for navbar and sidebar toggle
window.addEventListener('scroll', function() {
  const currentScrollPosition = window.pageYOffset || document.documentElement.scrollTop;
  const scrolled = currentScrollPosition > 100;
  
  // Show/hide sidebar toggle based on scroll position
  if (scrolled) {
      body.classList.add("scrolled");
  } else {
      body.classList.remove("scrolled");
      closeSidebarFunc();
  }
  
  // Navbar hide/show logic
  if (currentScrollPosition > lastScrollPosition && currentScrollPosition > navbarHeight) {
      // Scrolling down
      navbar.classList.add('hide-nav');
  } else {
      // Scrolling up
      if (currentScrollPosition < lastScrollPosition) {
          navbar.classList.remove('hide-nav');
      }
  }
  
  // At top of page
  if (currentScrollPosition <= 0) {
      navbar.classList.remove('hide-nav');
  }
  
  lastScrollPosition = currentScrollPosition;
});

// Initialize with scroll check on page load
document.addEventListener("DOMContentLoaded", function() {
  if (window.scrollY > 100) {
      body.classList.add("scrolled");
  } else {
      body.classList.remove("scrolled");
  }
  
  // Close sidebar when clicking on a link
  document.querySelectorAll('.sidebar-nav a').forEach(link => {
      link.addEventListener('click', closeSidebarFunc);
  });
});