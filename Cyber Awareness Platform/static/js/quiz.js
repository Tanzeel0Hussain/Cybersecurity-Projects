document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    const selects = [...form.querySelectorAll('select[name="q"]')];
    const unanswered = selects.some((select) => select.value === "");

    if (unanswered) {
      event.preventDefault();
      alert("Please answer all questions before generating your report.");
    }
  });
});
