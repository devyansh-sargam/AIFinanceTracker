"use client";

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { motion } from 'framer-motion';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { FiPlus, FiFilter, FiChevronLeft, FiSearch, FiTrash2, FiEdit2 } from 'react-icons/fi';

// Expense Item Component
const ExpenseItem = ({ expense, onEdit, onDelete }: { 
  expense: { 
    id: number, 
    description: string, 
    amount: number, 
    category: string, 
    date: string 
  }, 
  onEdit: (id: number) => void, 
  onDelete: (id: number) => void 
}) => {
  return (
    <motion.div 
      className="bg-gray-900/60 p-4 rounded-xl border border-gray-800 hover:border-emerald-500/50 
                transition-all duration-300 hover:shadow-lg hover:shadow-emerald-500/10"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.2 }}
    >
      <div className="flex justify-between items-center">
        <div>
          <h3 className="font-medium">{expense.description}</h3>
          <div className="flex items-center space-x-2 mt-1">
            <span className="text-xs px-2 py-1 rounded-full bg-gray-800">{expense.category}</span>
            <span className="text-xs text-gray-400">{expense.date}</span>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <span className="font-mono font-medium text-red-400">-${expense.amount.toFixed(2)}</span>
          <div className="flex space-x-2">
            <button 
              onClick={() => onEdit(expense.id)} 
              className="p-1.5 bg-gray-800 rounded-full hover:bg-gray-700 transition-colors"
            >
              <FiEdit2 className="h-4 w-4 text-gray-400" />
            </button>
            <button 
              onClick={() => onDelete(expense.id)} 
              className="p-1.5 bg-gray-800 rounded-full hover:bg-red-900/50 transition-colors"
            >
              <FiTrash2 className="h-4 w-4 text-gray-400 hover:text-red-400" />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default function ExpensesPage() {
  const { isLoaded, isSignedIn } = useUser();
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  // Sample expense data for demonstration
  const expenseData = [
    { id: 1, description: "Grocery Shopping", amount: 120.50, category: "Food", date: "Oct 10, 2023" },
    { id: 2, description: "Electric Bill", amount: 85.20, category: "Utilities", date: "Oct 5, 2023" },
    { id: 3, description: "Netflix Subscription", amount: 15.99, category: "Entertainment", date: "Oct 3, 2023" },
    { id: 4, description: "Gas", amount: 45.30, category: "Transportation", date: "Sep 30, 2023" },
    { id: 5, description: "Dentist Appointment", amount: 150.00, category: "Healthcare", date: "Sep 28, 2023" },
    { id: 6, description: "Restaurant Dinner", amount: 78.45, category: "Food", date: "Sep 25, 2023" },
    { id: 7, description: "Mobile Phone Bill", amount: 60.00, category: "Utilities", date: "Sep 20, 2023" },
    { id: 8, description: "Gym Membership", amount: 49.99, category: "Fitness", date: "Sep 15, 2023" },
  ];

  // Category filters for the dropdown
  const categories = ['all', 'food', 'utilities', 'entertainment', 'transportation', 'healthcare', 'fitness'];

  // Filter and search expenses
  const filteredExpenses = expenseData
    .filter(expense => filter === 'all' || expense.category.toLowerCase() === filter)
    .filter(expense => 
      expense.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      expense.category.toLowerCase().includes(searchTerm.toLowerCase())
    );

  // Handle edit expense
  const handleEditExpense = (id: number) => {
    console.log('Edit expense:', id);
    // Logic to edit expense would go here
  };

  // Handle delete expense
  const handleDeleteExpense = (id: number) => {
    console.log('Delete expense:', id);
    // Logic to delete expense would go here
  };

  // Handle authentication
  if (isLoaded && !isSignedIn) {
    redirect('/sign-in');
  }

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950">
        <div className="animate-pulse flex flex-col items-center">
          <div className="h-12 w-12 rounded-full bg-emerald-500/20 mb-4"></div>
          <div className="h-4 w-48 bg-emerald-500/20 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-black -z-10">
        <div className="absolute inset-0 overflow-hidden">
          <div 
            className="absolute -inset-[10px] opacity-50" 
            style={{
              background: 'radial-gradient(circle at top right, rgba(20, 184, 116, 0.1), transparent 40%)',
              filter: 'blur(40px)'
            }}
          />
          <div 
            className="absolute -inset-[10px] opacity-30" 
            style={{
              background: 'radial-gradient(circle at bottom left, rgba(0, 200, 150, 0.1), transparent 40%)',
              filter: 'blur(40px)'
            }}
          />
        </div>
      </div>
      
      {/* Header */}
      <header className="bg-gray-900/50 border-b border-gray-800 sticky top-0 z-10 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <Link href="/dashboard" className="flex items-center text-gray-300 hover:text-white mr-4">
                <FiChevronLeft className="h-5 w-5 mr-1" />
                <span>Back</span>
              </Link>
              <h1 className="text-xl font-bold text-white">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-500">
                  Expenses
                </span>
              </h1>
            </div>
          </div>
        </div>
      </header>
      
      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters and search */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div className="flex items-center space-x-2 bg-gray-900/60 rounded-lg p-2 border border-gray-800">
            <FiFilter className="h-5 w-5 text-gray-400" />
            <select 
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="bg-transparent border-none text-sm text-gray-300 focus:outline-none focus:ring-0"
            >
              {categories.map((category) => (
                <option key={category} value={category} className="bg-gray-900 text-gray-300">
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </option>
              ))}
            </select>
          </div>
          
          <div className="relative w-full md:w-64">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FiSearch className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              type="text" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search expenses..." 
              className="bg-gray-900/60 border border-gray-800 w-full pl-10 pr-4 py-2 rounded-lg text-gray-300 
                       focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>
        </div>
        
        {/* Expenses list */}
        <div className="space-y-4">
          {filteredExpenses.length > 0 ? (
            filteredExpenses.map((expense) => (
              <ExpenseItem 
                key={expense.id} 
                expense={expense} 
                onEdit={handleEditExpense} 
                onDelete={handleDeleteExpense} 
              />
            ))
          ) : (
            <div className="bg-gray-900/40 rounded-xl border border-gray-800 p-8 text-center">
              <p className="text-gray-400">No expenses found. Add a new expense to get started.</p>
            </div>
          )}
        </div>
        
        {/* Add expense button */}
        <div className="fixed bottom-8 right-8">
          <motion.button 
            className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700
                     text-white p-4 rounded-full shadow-lg hover:shadow-emerald-500/30 
                     transition-all duration-300 hover:scale-110 glow-effect"
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
          >
            <FiPlus className="h-6 w-6" />
          </motion.button>
        </div>
      </main>
    </div>
  );
}