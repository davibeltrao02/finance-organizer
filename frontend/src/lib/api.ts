const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// --- Tipos ---

export type TransactionType = "income" | "expense";

export interface Transaction {
  id: number;
  description: string;
  amount: number;
  type: TransactionType;
  category: string;
  transaction_date: string;
  created_at: string;
}

export interface Balance {
  total_income: number;
  total_expense: number;
  balance: number;
}

export interface CategoryTotal {
  category: string;
  total: number;
}

export interface ChatResponse {
  reply: string;
  transaction: Transaction | null;
}

// --- Funções ---

export async function getBalance(): Promise<Balance> {
  const res = await fetch(`${API_URL}/summary/balance`);
  return res.json();
}

export async function getByCategory(year: number, month: number): Promise<CategoryTotal[]> {
  const res = await fetch(`${API_URL}/summary/by-category?year=${year}&month=${month}`);
  return res.json();
}

export async function getTransactions(): Promise<Transaction[]> {
  const res = await fetch(`${API_URL}/transactions/`);
  return res.json();
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  return res.json();
}
