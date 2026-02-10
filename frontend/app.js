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

  if (!txnId) return;

  explanation.textContent = "Analyzing transaction with GenAI...";
  txnDetails.textContent = "";

  const res = await fetch(`${API_URL}/transaction/${txnId}/explain`);
  const data = await res.json();

  txnDetails.textContent = JSON.stringify(data.transaction, null, 2);

  if (!data.explanations || data.explanations.length === 0) {
    explanation.textContent = "No unusual behavior detected.";
    return;
  }

  explanation.innerHTML = data.explanations
    .map(e => `• ${e.explanation}`)
    .join("<br><br>");
}


// -----------------------------
explainBtn.addEventListener("click", explainTransaction);
loadTransactions();


const generateBtn = document.getElementById("generateBtn");

// Generate New Transaction
async function generateNewTransaction() {
  generateBtn.disabled = true;
  generateBtn.textContent = "Generating transaction...";

  try {
    const res = await fetch(`${API_URL}/generate-transaction`, {
      method: "POST"
    });

    const data = await res.json();

    if (data.status !== "OK") {
      alert("Failed to generate transaction");
      return;
    }

    // Reload transaction list
    await loadTransactions();
    explanation.textContent = "New transaction generated. Select it to explain.";
    txnDetails.textContent = "";

  } catch (err) {
    alert("Backend error while generating transaction");
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "➕ Generate New Transaction";
  }
}

generateBtn.addEventListener("click", generateNewTransaction);
