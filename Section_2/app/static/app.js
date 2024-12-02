document.addEventListener("DOMContentLoaded", function () {
    // Show Password when checkbox is clicked on
    const togglePassword = document.getElementById("togglePassword");
    if (togglePassword) {
        togglePassword.addEventListener("change", function () {
            // Show all password fields in the 'password-field' class
            const passwordFields = document.querySelectorAll(".password-field");
            passwordFields.forEach((field) => {
                field.type = this.checked ? "text" : "password";
            });
        });
    }

    // Validates the login form to ensure both fields are filled correctly
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        // Ensures login form fields are valid
        loginForm.addEventListener("submit", function (e) {
            const username = document.getElementById("username")?.value.trim();
            const password = document.getElementById("password")?.value.trim();

            // Disable submit button if fields are empty
            if (!username || !password) {
                e.preventDefault();
                alert("Please enter both username and password.");
            }
        });
    }

    // Favorites functionality for reviews
    document.querySelectorAll(".favorite-btn").forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Sends a request to add the review to favorites and shows an alert depending on user action
            fetch(`/add_to_favorites/${reviewId}`, {
                method: "POST",
            })
                .then((response) => response.json())
                .then((data) => {
                    // Adds to favorites if not already in favorites, shows alert otherwise
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

            // Sends a request to remove the review from favorites and shows an alert
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
            e.preventDefault();
            const card = e.target.closest(".review-card");
            const reviewId = card.dataset.id;

            // Confirms deletion after sending a delete request and shows error in any other case
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

    // Search functionality using AJAX
    const searchInput = document.getElementById("search-input");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            const query = searchInput.value.toLowerCase().trim();
            const cards = document.querySelectorAll(".review-card");

            // If the search bar has no character input, show all cards and remove highlights
            if (!query) {
                const noResultsMessage = document.getElementById("no-results-message");
                cards.forEach((card) => {
                    card.style.display = "flex";
                    resetHighlights(card);
                });

                // Remove "No results found" message if the character typed in exists in a card
                if (noResultsMessage) {
                    noResultsMessage.remove();
                }
                return;
            }

            // Send an AJAX request to search results
            fetch(`/search_results?query=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
                .then((response) => response.json())
                .then((data) => {
                    let hasResults = false;

                    // Show/hide cards based on the characters inputted
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

                    // Show no results message if no results are found
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

        // Function to highlight matching characters in the text
        function highlightMatches(card, query) {
            const elements = card.querySelectorAll("h3, p, strong");
            elements.forEach((el) => {
                const originalText = el.textContent;
                const regex = new RegExp(`(${query})`, "gi");

                if (el.tagName === "STRONG") {
                    el.innerHTML = originalText;
                } else {
                    el.innerHTML = originalText.replace(regex, "<mark>$1</mark>");
                }
            });
        }

        // Function to bring back highlighted characters to original text
        function resetHighlights(card) {
            const elements = card.querySelectorAll("h3, p, strong");
            elements.forEach((el) => {
                el.innerHTML = el.textContent;
            });
        }
    }
});