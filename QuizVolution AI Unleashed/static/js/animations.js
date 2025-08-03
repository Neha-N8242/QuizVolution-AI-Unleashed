document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector(".animation-container");
    const symbols = ["{}", "[]", "<>", "()", ";", "=>", "#", "$", "&"];
    
    function createSymbol() {
        const symbol = document.createElement("span");
        symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
        symbol.style.position = "absolute";
        symbol.style.color = `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.7)`;
        symbol.style.fontSize = `${Math.random() * 20 + 10}px`;
        symbol.style.left = `${Math.random() * 100}vw`;
        symbol.style.top = `${Math.random() * 100}vh`;
        symbol.style.animation = `float ${Math.random() * 5 + 3}s linear infinite`;
        container.appendChild(symbol);
        
        setTimeout(() => symbol.remove(), 5000);
    }
    
    setInterval(createSymbol, 500);
});

const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% { transform: translateY(0); opacity: 1; }
        100% { transform: translateY(-100vh); opacity: 0; }
    }
`;
document.head.appendChild(style);