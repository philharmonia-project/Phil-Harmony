/*==================== SIDEBAR DROPDOWN ====================*/
document.querySelectorAll('.sidebar__dropdown-toggle').forEach(toggle => {
    toggle.addEventListener('click', function () {
        const parent = this.parentElement;
        const isOpen = parent.classList.contains('open');

        document.querySelectorAll('.sidebar__item').forEach(item => item.classList.remove('open'));
        if (!isOpen) parent.classList.add('open');
    });
});

/*==================== REMEMBER ACTIVE SECTION ====================*/
function setActiveSection(sectionId) {
    localStorage.setItem("activeSection", sectionId);
}

function getActiveSection() {
    return localStorage.getItem("activeSection") || "admin-dashboard";
}

/*==================== MAIN SIDEBAR NAVIGATION ====================*/
document.addEventListener("DOMContentLoaded", () => {

    /* ALL YOUR LINK + CONTENT VARIABLES HERE */
    const sections = {
        "admin-dashboard": document.getElementById("admin-dashboard"),
        "admin_threeD": document.getElementById("admin_threeD"),
        "admin_3dContent": document.getElementById("admin_3dContent"),
        "admin-Instrument": document.getElementById("admin-Instrument"),
        "admin-InsImage": document.getElementById("admin-InsImage"),
        "admin-History": document.getElementById("admin-History"),
        "admin-InsLink": document.getElementById("admin-InsLink"),
        "Category": document.getElementById("Category"),
        "admin-Tribe": document.getElementById("admin-Tribe"),
        "admin-Sound": document.getElementById("admin-Sound"),
        "admin-Material": document.getElementById("admin-Material"),
        "admin-Construction": document.getElementById("admin-Construction"),
        "admin-Tutorial": document.getElementById("admin-Tutorial"),
        "admin-PlayingGuide": document.getElementById("admin-PlayingGuide"),
        "admin-Significance": document.getElementById("admin-Significance"),
        "admin-FunFact": document.getElementById("admin-FunFact"),
        "admin-HomePage": document.getElementById("admin-HomePage"),
        "admin-Principle": document.getElementById("admin-Principle"),
        "admin-Instructor": document.getElementById("admin-Instructor"),
        "admin-Offering": document.getElementById("admin-Offering"),
        "admin-CulturalImportance": document.getElementById("admin-CulturalImportance"),
        "admin-TargetAudience": document.getElementById("admin-TargetAudience"),
        "admin-TeamMember": document.getElementById("admin-TeamMember"),
        "admin-ContactPage": document.getElementById("admin-ContactPage"),
        "admin-ContactMessage": document.getElementById("admin-ContactMessage"),
        "admin-feedback": document.getElementById("admin-feedback"),
        "admin-testimonial": document.getElementById("admin-testimonial"),
        "admin-Appointment": document.getElementById("admin-Appointment"),
        "admin-Footer": document.getElementById("admin-Footer")
    };

    const links = document.querySelectorAll(".sidebar__link");

    /* HIDE EVERYTHING */
    function hideAll() {
        Object.values(sections).forEach(sec => sec.style.display = "none");
    }

    /* ACTIVATE A SECTION */
    function activateSection(id) {
        hideAll();
        if (sections[id]) sections[id].style.display = "block";

        links.forEach(link => link.classList.remove("active-link"));
        const activeLink = document.querySelector(`a[href='#${id}']`);
        if (activeLink) activeLink.classList.add("active-link");

        setActiveSection(id);
    }

    /* ADD CLICK EVENTS TO ALL LINKS */
    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const id = link.getAttribute("href").replace("#", "");
            activateSection(id);
        });
    });

    /* RESTORE LAST OPEN PAGE AFTER UPDATE/DELETE/CREATE */
    activateSection(getActiveSection());
});

/*==================== SHOW SIDEBAR ====================*/
const showSidebar = (toggleId, sidebarId, headerId, mainId) => {
    const toggle = document.getElementById(toggleId),
        sidebar = document.getElementById(sidebarId),
        header = document.getElementById(headerId),
        main = document.getElementById(mainId);

    if (toggle && sidebar && header && main) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('show-sidebar');
            header.classList.toggle('left-pd');
            main.classList.toggle('left-pd');
        });
    }
};
showSidebar('header-toggle', 'sidebar', 'header', 'main');

/*==================== DARK LIGHT THEME ====================*/
const themeButton = document.getElementById('theme-button');
const darkTheme = 'dark-theme';
const iconTheme = 'ri-sun-fill';

const selectedTheme = localStorage.getItem('selected-theme');
const selectedIcon = localStorage.getItem('selected-icon');

const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light';
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-clear-fill' : 'ri-sun-fill';

if (selectedTheme) {
    document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme);
    themeButton.classList[selectedIcon === 'ri-moon-clear-fill' ? 'add' : 'remove'](iconTheme);
}

themeButton.addEventListener('click', () => {
    document.body.classList.toggle(darkTheme);
    themeButton.classList.toggle(iconTheme);

    localStorage.setItem('selected-theme', getCurrentTheme());
    localStorage.setItem('selected-icon', getCurrentIcon());
});

  

  // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK 
    // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK   // CLOCK 
// JavaScript
function updateClock() {
    const now = new Date();
    // Convert to Philippine time (UTC+8)
    const phTime = new Date(now.getTime() + (now.getTimezoneOffset() * 60000) + (480 * 60000));
    
    const hours = phTime.getHours() % 12;
    const minutes = phTime.getMinutes();
    const seconds = phTime.getSeconds();
    
    const hourDeg = (hours * 30) + (minutes * 0.5);
    const minuteDeg = minutes * 6;
    const secondDeg = seconds * 6;
    
    document.querySelector('.hour-hand').style.transform = `rotate(${hourDeg}deg)`;
    document.querySelector('.minute-hand').style.transform = `rotate(${minuteDeg}deg)`;
    document.querySelector('.second-hand').style.transform = `rotate(${secondDeg}deg)`;
}

// Update immediately
updateClock();

// Update every second
setInterval(updateClock, 1000);


  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON
  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON  // LOGOUT BUTTON
  document.addEventListener('DOMContentLoaded', function() {
    const adminLogoutButton = document.getElementById('adminLogoutButton');
    const adminLogoutModal = document.getElementById('adminLogoutModal');
    const adminConfirmLogout = document.getElementById('adminConfirmLogout');
    const adminCancelLogout = document.getElementById('adminCancelLogout');
    
    // Handle logout button click
    adminLogoutButton.addEventListener('click', function(e) {
        e.preventDefault();
        adminLogoutModal.classList.add('show');
        document.body.style.overflow = 'hidden'; // Prevent scrolling when modal is open
    });
    
    // Handle confirm logout
    adminConfirmLogout.addEventListener('click', function() {
        adminLogoutModal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    });
    
    // Handle cancel logout
    adminCancelLogout.addEventListener('click', function() {
        adminLogoutModal.classList.remove('show');
        document.body.style.overflow = ''; // Restore scrolling
    });
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === adminLogoutModal) {
            adminLogoutModal.classList.remove('show');
            document.body.style.overflow = ''; // Restore scrolling
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && adminLogoutModal.classList.contains('show')) {
            adminLogoutModal.classList.remove('show');
            document.body.style.overflow = ''; // Restore scrolling
        }
    });
});