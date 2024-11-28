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
        // Ensures login form fields are filled before submitting
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
                        alert("An error occurred when adding the review.");
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
                        alert("Item moved from your favorites.");
                        card.remove();
                    } else {
                        alert("An error occurred when moving the card.");
                    }
                })
                .catch(() => {
                    alert("An error occured! Failed to remove from favorites.");
                });
        });
    });

    // Delete functionality
    document.querySelectorAll(".delete-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default form submission behavior
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Confirms deletion before sending a delete request
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

    // Search functionality with real-time AJAX
    const searchInput = document.getElementById("search-input");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase().trim();
            const cards = document.querySelectorAll(".review-card");

            // If the search query is empty, display all cards and reset highlights
            if (!query) {
                const noResultsMessage = document.getElementById("no-results-message");

                // Show all cards and reset highlights
                cards.forEach((card) => {
                    card.style.display = "flex";
                    resetHighlights(card);
                });

                // Remove "No results found" message if it exists
                if (noResultsMessage) {
                    noResultsMessage.remove();
                }
                return; // Exit the function early since no search is needed
            }

            // Send an AJAX request to the search_results endpoint
            fetch(`/search_results?query=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    let hasResults = false;

                    // Show/hide cards based on the returned IDs
                    cards.forEach((card) => {
                        const reviewId = parseInt(card.dataset.id);
                        if (data.results.some(result => result.id === reviewId)) {
                            card.style.display = "flex";
                            highlightMatches(card, query);
                            hasResults = true;
                        } else {
                            card.style.display = "none";
                        }
                    });

                    // Handle no results message
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
                })
                .catch(() => {
                    alert("Failed to perform search. Please try again later.");
                });
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

        // Function to reset highlights to original text
        function resetHighlights(card) {
            const elements = card.querySelectorAll("h3, p, strong");
            elements.forEach((el) => {
                el.innerHTML = el.textContent;
            });
        }
    }
});