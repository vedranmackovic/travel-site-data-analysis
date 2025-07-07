document.getElementById('chart-search').addEventListener('change', function () {
    const selectedId = this.value;
    const target = document.getElementById(selectedId);
    if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        target.classList.add("highlight");
        setTimeout(() => target.classList.remove("highlight"), 2000);
    }
});
window.addEventListener("load", function () {
    const hash = window.location.hash;
    const validHashes = ["#monthly-trends", "#monthly-total-cost"];
    
    if (validHashes.includes(hash)) {
        const el = document.querySelector(hash);
        if (el) {
            setTimeout(() => {
                el.scrollIntoView({ behavior: "smooth", block: "end" });
                el.classList.add("highlight");
                setTimeout(() => el.classList.remove("highlight"), 2000);
            }, 300);
        }
    }
});