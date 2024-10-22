// js of signup and login page
// Handle sign-up form submission
document.getElementById("signup-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/auth/signup", {  // Adjusted to the correct endpoint
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Account created successfully! Redirecting to login...");
            window.location.href = "/login";  // Adjusted URL
        } else {
            alert(data.detail || "Sign up failed");
        }
    } catch (err) {
        console.error("Error during sign up:", err);
    }
});

// Handle login form submission
document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("email").value; // assuming using email
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("/auth/login", {  // Adjusted to the correct endpoint
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "/dashboard";  // Adjusted URL
        } else {
            alert(data.detail || "Login failed");
        }
    } catch (err) {
        console.error("Error logging in:", err);
    }
});


// js of dashboard.html
// Function to fetch and display loan overview
async function loadDashboard() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "login.html";
        return;
    }

    const response = await fetch("/account_overview/{customer_id}", {
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    const loans = await response.json();
    const loansOverview = document.getElementById("loans-overview");

    loansOverview.innerHTML = "";
    loans.forEach(loan => {
        loansOverview.innerHTML += `
            <div class="loan">
                <p>Loan ID: ${loan.loan_id}</p>
                <p>Loan Amount: ${loan.loan_amount}</p>
                <p>Total Amount: ${loan.total_amount}</p>
                <p>EMI: ${loan.emi}</p>
                <p>Status: ${loan.status}</p>
                <p>EMIs Left: ${loan.emi_left}</p>
                <a href="ledger.html?loan_id=${loan.loan_id}">View Ledger</a>
            </div>
        `;
    });
}

// Call this on page load
loadDashboard();

// Logout functionality
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// js of apply-loan.html
document.getElementById("loan-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const loanAmount = document.getElementById("loan_amount").value;
    const loanPeriod = document.getElementById("loan_period").value;
    const rateOfInterest = document.getElementById("rate_of_interest").value;

    const token = localStorage.getItem("token");

    try {
        const response = await fetch("/lend", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                customer_id: "12345678",  // Replace with dynamic customer_id
                loan_amount: loanAmount,
                loan_period: loanPeriod,
                rate_of_interest: rateOfInterest
            })
        });

        const data = await response.json();
        if (response.ok) {
            alert("Loan applied successfully! Loan ID: " + data.loan_id);
        } else {
            alert(data.detail || "Loan application failed");
        }
    } catch (err) {
        console.error("Error applying for loan:", err);
    }
});

