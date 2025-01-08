function toggleMenu() {
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.nav-container');
  
  hamburger.classList.toggle('active');
  nav.classList.toggle('active');
}

// Cerrar menú al hacer clic en un enlace
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('click', () => {
      const hamburger = document.querySelector('.hamburger');
      const nav = document.querySelector('.nav-container');
      
      hamburger.classList.remove('active');
      nav.classList.remove('active');
  });
});

// Cerrar menú al hacer clic fuera
document.addEventListener('click', (e) => {
  const hamburger = document.querySelector('.hamburger');
  const nav = document.querySelector('.nav-container');
  
  if (!hamburger.contains(e.target) && !nav.contains(e.target)) {
      hamburger.classList.remove('active');
      nav.classList.remove('active');
  }
});