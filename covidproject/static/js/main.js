
document.addEventListener("DOMContentLoaded", function (event) {
	var currentPath = this.location.pathname;
	var navLinks = document.getElementsByClassName('nav-link')
	for (var i = 0, len = navLinks.length; i < len; i++) {
		if (navLinks[i].getAttribute("href") === currentPath) {
			navLinks[i].parentElement.className += ' active'
			console.log(navLinks[i].parentElement)
			console.log(navLinks[i].parentElement.className)
		}
	}
})

