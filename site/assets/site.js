document.getElementById("year").textContent = String(new Date().getFullYear());

const currentLink = document.querySelector('.site-header nav a[href="#agents"]');
const machineSection = document.getElementById("agents");

if (currentLink && machineSection && "IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    entries => {
      const visible = entries.some(entry => entry.isIntersecting);
      currentLink.toggleAttribute("aria-current", visible);
    },
    { threshold: 0.35 },
  );
  observer.observe(machineSection);
}
