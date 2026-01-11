document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    if (!form) return;

    form.addEventListener("submit", (e) => {
        const selects = document.querySelectorAll("select");
        let answered = true;

        selects.forEach(sel => {
            if (sel.value === "") {
                answered = false;
            }
        });

        if (!answered) {
            e.preventDefault();
            alert("⚠️ Please answer all questions before submitting!");
        }
    });
});
