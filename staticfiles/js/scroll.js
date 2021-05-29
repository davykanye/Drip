const header = document.querySelector("header");
const sectionOne = document.querySelector(".container.x");

const sectionOneOptions = {
	rootMargin: "-10%"
};

const sectionOneObserver = new IntersectionObserver(function(entries, sectionOneObserver) 
{
	entries.forEach(entry => {
		if(entry.isIntersecting) {
			header.classList.add("scrolled");
		} else {
			header.classList.remove("scrolled");
		}
	});
}, sectionOneOptions);

sectionOneObserver.observe(sectionOne);