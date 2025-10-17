// Array of input IDs
const inputIds = ['fname', 'lname', 'email', 'phone'];

inputIds.forEach(id => {
    const input = document.getElementById(id);
    input.addEventListener('input', () => {
        input.setAttribute('value', input.value);
    });
});

// Prevent scrolling for parent iframe
parent.document.getElementsByTagName('iframe')[0].scrolling = "no";
