
export function handleClick(event) {
    event.preventDefault(); 
    window.location.href = "./dashboard.html"; 
}

document.getElementById('login').addEventListener('click', handleClick);
