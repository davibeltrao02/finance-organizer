"use client";

import { getTransactions, Transaction } from "@/lib/api";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useEffect, useState } from "react";

export default function SobrePage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  useEffect(() => {
    getTransactions().then(setTransactions);
  }, []);

  return (
    <div>
      <h1>Transações</h1>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Data</TableHead>
            <TableHead>Descrição</TableHead>
            <TableHead>Categoria</TableHead>
            <TableHead>Tipo</TableHead>
            <TableHead>Valor</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {transactions.map((t) => (
            <TableRow key={t.id}>
              <TableCell>
                {new Date(t.transaction_date).toLocaleDateString("pt-BR")}
              </TableCell>
              <TableCell>{t.description}</TableCell>
              <TableCell>{t.category}</TableCell>
              <TableCell>
                {t.type === "income" ? "Receita" : "Despesa"}
              </TableCell>
              <TableCell
                className={
                  t.type === "income" ? "text-green-600" : "text-red-500"
                }
              >
                R$ {t.amount.toFixed(2)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
