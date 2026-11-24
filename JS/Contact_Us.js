// Keep each input's value attribute in sync so the floating labels stay up once filled
document.querySelectorAll('form .input-container input').forEach(input => {
    input.addEventListener('input', () => {
        input.setAttribute('value', input.value);
    });
});

// Prevent scrolling for parent iframe
parent.document.getElementsByTagName('iframe')[0].scrolling = "no";
