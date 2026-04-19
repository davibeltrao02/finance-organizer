"use client";

import { useEffect, useState } from "react";
import { getBalance, getByCategory, Balance, CategoryTotal } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import Link from "next/link";

const COLORS = [
  "#6366f1",
  "#f59e0b",
  "#10b981",
  "#ef4444",
  "#3b82f6",
  "#8b5cf6",
  "#ec4899",
];

export default function DashboardPage() {
  const now = new Date();

  const [balance, setBalance] = useState<Balance | null>(null);
  const [categories, setCategories] = useState<CategoryTotal[]>([]);

  useEffect(() => {
    getBalance().then(setBalance);
    getByCategory(now.getFullYear(), now.getMonth() + 1).then(setCategories);
  }, []);

  return (
    <main className="p-8 max-w-5xl mx-auto">
      <Link
        href="/transactions/"
        className="mb-4 inline-block px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Transações
      </Link>

      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      {/* Cards de resumo */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-gray-500">Receitas</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-green-600">
              R$ {balance?.total_income.toFixed(2) ?? "..."}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-gray-500">Despesas</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold text-red-500">
              R$ {balance?.total_expense.toFixed(2) ?? "..."}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-sm text-gray-500">Saldo</CardTitle>
          </CardHeader>
          <CardContent>
            <p
              className={`text-2xl font-bold ${(balance?.balance ?? 0) >= 0 ? "text-blue-600" : "text-red-600"}`}
            >
              R$ {balance?.balance.toFixed(2) ?? "..."}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráfico de pizza por categoria */}
      {/* TODO: Implemente o gráfico abaixo usando o componente PieChart do recharts.
          Você tem disponível:
          - `categories`: array de { category: string, total: number }
          - Os componentes importados: PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer
          - COLORS: array de cores para cada fatia

          Dicas:
          1. Envolva tudo em <ResponsiveContainer width="100%" height={350}>
          2. Dentro, use <PieChart>
          3. Dentro do PieChart, use <Pie data={categories} dataKey="total" nameKey="category">
          4. Dentro do Pie, mapeie COLORS com <Cell key={i} fill={COLORS[i % COLORS.length]} />
          5. Adicione <Tooltip /> e <Legend /> fora do Pie mas dentro do PieChart

          Documentação: https://recharts.org/en-US/api/PieChart
      */}
      <Card>
        <CardHeader>
          <CardTitle>Gastos por Categoria</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={categories}
                dataKey="total"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={100}
                fill="#8884d8"
                label
              >
                {categories.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </main>
  );
}
