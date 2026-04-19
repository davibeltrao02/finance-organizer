"use client";

import {
  getTransactions,
  updateTransaction,
  TransactionType,
  getCategories,
} from "@/lib/api";
import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import { get } from "http";

export default function EditPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const router = useRouter();
  // 1. Estado do formulário
  const [form, setForm] = useState({
    description: "",
    amount: 0,
    transaction_date: "",
    category: "",
    type: "income" as TransactionType,
  });

  const [categories, setCategories] = useState<string[]>([]);

  useEffect(() => {
    getTransactions().then((transactions) => {
      const t = transactions.find((t) => t.id === Number(id));
      if (t) {
        setForm(t);
        getCategories(t.type).then(setCategories); // ← adiciona isso
      }
    });
  }, []);

  async function handleSubmit() {
    await updateTransaction(Number(id), form);
    router.push("/transactions");
  }

  // 4. Renderiza o formulário
  return (
    <form>
      <label>Descrição</label>
      <input
        value={form.description}
        onChange={(e) => setForm({ ...form, description: e.target.value })}
      />
      <label>Valor</label>
      <input
        type="number"
        value={form.amount}
        onChange={(e) => setForm({ ...form, amount: Number(e.target.value) })}
      />
      <label>Data</label>
      <input
        type="date"
        value={form.transaction_date}
        onChange={(e) => setForm({ ...form, transaction_date: e.target.value })}
      />
      <label>Categoria</label>
      <select
        value={form.category}
        onChange={(e) => setForm({ ...form, category: e.target.value })}
      >
        {categories.map((cat) => (
          <option key={cat} value={cat}>
            {cat}
          </option>
        ))}
      </select>
      <select
        value={form.type}
        onChange={(e) => {
          const newType = e.target.value as TransactionType;
          setForm({ ...form, type: newType });
          getCategories(newType).then(setCategories); // ← atualiza categorias
        }}
      >
        <option value="income">Receita</option>
        <option value="expense">Despesa</option>
      </select>
      <button type="button" onClick={handleSubmit}>
        Salvar
      </button>
    </form>
  );
}
