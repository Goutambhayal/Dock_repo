document.addEventListener('click', function (event) {
    const link = event.target.closest('.dynamic-link');
    if (!link) return;

    event.preventDefault();
    const url = link.href;

    fetch(url)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return response.text();
        })
        .then(html => {
            const container = document.getElementById('dynamic-content');
            container.innerHTML = html;

            // Auto-run if All Companies page is loaded
            if (container.querySelector('#companyList') && typeof initAllCompanies === 'function') {
                initAllCompanies();
            }
        })
        .catch(err => console.error('Error loading content:', err));
});
