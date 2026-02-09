const API_URL = "http://127.0.0.1:8000";

const txnSelect = document.getElementById("txnSelect");
const explainBtn = document.getElementById("explainBtn");
const txnDetails = document.getElementById("txnDetails");
const explanation = document.getElementById("explanation");

// Load Transactions
async function loadTransactions() {
  const res = await fetch(`${API_URL}/transactions?limit=1000`);
  const data = await res.json();

  if (data.length === 0) {
    txnSelect.innerHTML = `<option>No transactions found</option>`;
    explainBtn.disabled = true;
    return;
  }

  txnSelect.innerHTML = "";

  data.forEach(txn => {
    const option = document.createElement("option");
    option.value = txn.transaction_id;
    option.textContent = `${txn.transaction_id} • RM${txn.amount} • ${txn.category}`;
    txnSelect.appendChild(option);
  });
}

// Explain Transaction
async function explainTransaction() {
  const txnId = txnSelect.value;

  if (!txnId) {
    alert("No transaction selected");
    return;
  }

  explanation.textContent = "Analyzing transaction...";
  txnDetails.textContent = "";

  const res = await fetch(`${API_URL}/transaction/${txnId}/explain`);
  const data = await res.json();

  txnDetails.textContent = JSON.stringify(data.transaction, null, 2);

  explanation.textContent = data.explanation
    ? data.explanation.explanation
    : "No unusual behavior detected.";
}

// -----------------------------
explainBtn.addEventListener("click", explainTransaction);
loadTransactions();
