// mark the navbar items when it is active 
document.addEventListener("DOMContentLoaded", function (event) {
	const currentPath = this.location.pathname;
	const navLinks = document.getElementsByClassName('nav-link')
	for (let i = 0, len = navLinks.length; i < len; i++) {
		if (navLinks[i].getAttribute("href") === currentPath) {
			navLinks[i].parentElement.className += ' active'
			console.log(navLinks[i].parentElement)
			console.log(navLinks[i].parentElement.className)
		}
	}
})
