/* ========================================================================================== */
/* =====                                    SHOW NAVBAR                                 ===== */
/* ========================================================================================== */

const showNavbar = (toggleId, wrapperSidebar) => {
    const toggle = document.getElementById(toggleId)
    const wrapper = document.getElementById(wrapperSidebar)

    // Validate that all variables exist
    if (toggle && wrapper) {

        toggle.addEventListener('click', () => {
            // show navbar
            wrapper.classList.toggle('show')
        })
    }
}

showNavbar('button-bar', 'wrapper')