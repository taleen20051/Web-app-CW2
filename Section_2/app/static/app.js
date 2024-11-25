document.addEventListener("DOMContentLoaded", function () {
    // Password visibility toggle
    const passwordField = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");
    if (togglePassword && passwordField) {
        // Toggles password visibility when the checkbox is clicked
        togglePassword.addEventListener("change", function () {
            passwordField.type = this.checked ? "text" : "password";
        });
    }

    // Form validation for login button
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        // Makes sure of login form fields before submitting
        loginForm.addEventListener("submit", function (e) {
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();

            // Blocks submission if fields are empty
            if (!username || !password) {
                e.preventDefault();
                alert("Please enter both username and password.");
            }
        });
    }

    // Favorites functionality
    document.querySelectorAll(".favorite-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Sends a request to add the review to favorites and displays an alert
            fetch(`/add_to_favorites/${reviewId}`, {
                method: "POST",
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.message === "Already in favorites") {
                        alert("This item is already in your favorites!");
                    } else if (data.message === "Added to favorites") {
                        alert("Item added to your favorites!");
                    } else {
                        alert("An unexpected error occurred.");
                    }
                })
                .catch(() => {
                    alert("Failed to add to favorites. Please try again later.");
                });
        });
    });

    // Unfavorite functionality
    document.querySelectorAll(".unfavorite-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Sends a request to remove the review from favorites and displays an alert
            fetch(`/remove_from_favorites/${reviewId}`, {
                method: "POST",
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.message === "Removed from favorites") {
                        alert("Item removed from your favorites.");
                        card.remove();
                    } else {
                        alert("An unexpected error occurred.");
                    }
                })
                .catch(() => {
                    alert("Failed to remove from favorites. Please try again later.");
                });
        });
    });

    // Delete functionality
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default form submission behavior
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Confirms deletion after(before) sending a delete request
            if (confirm("Are you sure you want to delete this review?")) {
                fetch(`/delete_review/${reviewId}`, {
                    method: "POST",
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.message === "Review deleted") {
                            alert("Review deleted successfully.");
                            card.remove();
                        } else {
                            alert("An unexpected error occurred.");
                        }
                    })
                    .catch(() => {
                        alert("Failed to delete the review. Please try again later.");
                    });
            }
        });
    });

    // Search functionality
    const searchInput = document.getElementById("search-input");
    const searchButton = document.getElementById("search-btn");

    if (searchInput && searchButton) {
        // Filters and highlights review cards based on text query
        searchButton.addEventListener("click", function () {
            const query = searchInput.value.toLowerCase().trim();
            const cards = document.querySelectorAll(".review-card");
            let hasResults = false;

            // Filters and highlights matching cards to search input
            cards.forEach((card) => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = "flex";
                    highlightMatches(card, query);
                    hasResults = true;
                } else {
                    card.style.display = "none";
                }
            });

            // Displays an empty message when no results are found
            const noResultsMessage = document.getElementById("no-results-message");
            if (!hasResults) {
                if (!noResultsMessage) {
                    const message = document.createElement("div");
                    message.id = "no-results-message";
                    message.textContent = "No results found.";
                    document.querySelector(".grid").appendChild(message);
                }
            } else {
                if (noResultsMessage) {
                    noResultsMessage.remove();
                }
            }
        });

        // Resets the card visibility and remove highlights when clearing the search
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase().trim();
            const cards = document.querySelectorAll(".review-card");
            const noResultsMessage = document.getElementById("no-results-message");

            cards.forEach((card) => {
                resetHighlights(card);
                if (!query) {
                    card.style.display = "flex";
                }
            });

            if (!query && noResultsMessage) {
                noResultsMessage.remove();
            }
        });

        // Function to highlight card matches in the text
        function highlightMatches(card, query) {
            const elements = card.querySelectorAll("h3, p, strong");
            elements.forEach((el) => {
                const originalText = el.textContent;
                const regex = new RegExp(`(${query})`, "gi");

                if (el.tagName === "STRONG") {
                     // Keeps bold styling for <strong> elements
                    el.innerHTML = originalText;
                } else {
                    el.innerHTML = originalText.replace(regex, "<mark>$1</mark>");
                }
            });
        }

        // Function that reset highlights to original text
        function resetHighlights(card) {
            const elements = card.querySelectorAll("h3, p");
            elements.forEach((el) => {
                el.innerHTML = el.textContent;
            });
        }
    }
});