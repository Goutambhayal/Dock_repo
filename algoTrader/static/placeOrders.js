document.addEventListener("DOMContentLoaded", function () {
    const dynamicLinks = document.querySelectorAll(".dynamic-link");
    const contentContainer = document.getElementById("dynamic-content");

    dynamicLinks.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            const url = this.getAttribute("data-url");
            fetch(url)
                .then(response => {
                    if (!response.ok) throw new Error("Network error");
                    return response.text();
                })
                .then(html => {
                    contentContainer.innerHTML = html;
                })
                .catch(error => {
                    contentContainer.innerHTML = `<p class="text-danger">Failed to load content.</p>`;
                    console.error("Error loading dynamic content:", error);
                });
        });
    });
    
});
