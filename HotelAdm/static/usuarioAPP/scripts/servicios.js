document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".servicios-card");

    // Función para actualizar las tarjetas al hacer clic
    const updateCards = (activeIndex) => {
        cards.forEach((card, index) => {
            if (index === activeIndex) {
                card.classList.add("active");
                card.style.zIndex = "2"; // Llevar al frente
            } else {
                card.classList.remove("active");
                card.style.zIndex = "1"; // Enviar al fondo
            }
        });
    };

    // Evento de clic para cada tarjeta
    cards.forEach((card, index) => {
        card.addEventListener("click", () => {
            updateCards(index);
        });
    });

    // Inicializar la tarjeta central como activa
    updateCards(1); // Índice de la tarjeta inicial activa
});
