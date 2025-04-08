"use client";

import { useState, useEffect } from 'react';
import { useUser } from '@clerk/nextjs';
import { motion } from 'framer-motion';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { FiPieChart, FiDollarSign, FiTarget, FiTrendingUp, FiPlus } from 'react-icons/fi';

// Dashboard Widget Component
const DashboardWidget = ({ title, value, icon, color }: { title: string, value: string | number, icon: React.ReactNode, color: string }) => {
  return (
    <motion.div 
      className="bg-gray-900/60 p-6 rounded-xl border border-gray-800 shadow-lg glow-effect hover-scale"
      whileHover={{ y: -5 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center space-x-4">
        <div className={`p-3 rounded-lg ${color}`}>
          {icon}
        </div>
        <div>
          <p className="text-gray-400 text-sm">{title}</p>
          <h3 className="text-2xl font-bold">{value}</h3>
        </div>
      </div>
    </motion.div>
  );
};

// Card Component
const Card = ({ title, children, className = '' }: { title: string, children: React.ReactNode, className?: string }) => {
  return (
    <motion.div 
      className={`bg-gray-900/60 rounded-xl border border-gray-800 shadow-lg overflow-hidden ${className}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="border-b border-gray-800 px-6 py-4">
        <h3 className="font-medium text-lg">{title}</h3>
      </div>
      <div className="p-6">
        {children}
      </div>
    </motion.div>
  );
};

export default function Dashboard() {
  const { isLoaded, isSignedIn, user } = useUser();
  const [loading, setLoading] = useState(true);
  
  // Placeholder data for demonstration
  const dashboardData = {
    totalExpenses: "$2,540.32",
    totalIncome: "$5,200.00",
    savingsRate: "24%",
    budgetProgress: "62%",
  };
  
  // Recent transactions (placeholder)
  const recentTransactions = [
    { id: 1, description: "Grocery Shopping", amount: "-$120.50", date: "Today", category: "Food" },
    { id: 2, description: "Salary Deposit", amount: "+$3,200.00", date: "Yesterday", category: "Income" },
    { id: 3, description: "Electric Bill", amount: "-$85.20", date: "Sep 5, 2023", category: "Utilities" },
    { id: 4, description: "Freelance Work", amount: "+$650.00", date: "Sep 3, 2023", category: "Income" },
  ];
  
  // Budget categories (placeholder)
  const budgetCategories = [
    { id: 1, category: "Housing", spent: 1200, budget: 1500, percentage: 80 },
    { id: 2, category: "Food", spent: 420, budget: 600, percentage: 70 },
    { id: 3, category: "Transport", spent: 280, budget: 400, percentage: 70 },
    { id: 4, category: "Entertainment", spent: 150, budget: 300, percentage: 50 },
  ];

  // Simulate loading effect
  useEffect(() => {
    if (isLoaded) {
      const timer = setTimeout(() => {
        setLoading(false);
      }, 1000);
      return () => clearTimeout(timer);
    }
  }, [isLoaded]);

  // Handle authentication
  if (isLoaded && !isSignedIn) {
    redirect('/sign-in');
  }

  if (!isLoaded || loading) {
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
              <h1 className="text-xl font-bold text-white">
                <Link href="/dashboard" className="flex items-center">
                  <span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-500">
                    AI Finance Dashboard
                  </span>
                </Link>
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-300">
                Welcome, {user?.firstName || 'User'}
              </div>
              <img 
                src={user?.imageUrl || 'https://via.placeholder.com/40'} 
                alt="Profile" 
                className="w-8 h-8 rounded-full border border-gray-700" 
              />
            </div>
          </div>
        </div>
      </header>
      
      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome section */}
        <motion.div 
          className="mb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-3xl font-bold">Welcome back, {user?.firstName || 'User'}</h1>
          <p className="text-gray-400 mt-1">Here's an overview of your finances</p>
        </motion.div>
        
        {/* Dashboard widgets */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <DashboardWidget 
            title="Total Expenses" 
            value={dashboardData.totalExpenses} 
            icon={<FiDollarSign className="h-6 w-6 text-white" />} 
            color="bg-red-500/20"
          />
          <DashboardWidget 
            title="Total Income" 
            value={dashboardData.totalIncome} 
            icon={<FiTrendingUp className="h-6 w-6 text-white" />} 
            color="bg-emerald-500/20"
          />
          <DashboardWidget 
            title="Savings Rate" 
            value={dashboardData.savingsRate} 
            icon={<FiPieChart className="h-6 w-6 text-white" />} 
            color="bg-blue-500/20"
          />
          <DashboardWidget 
            title="Budget Progress" 
            value={dashboardData.budgetProgress} 
            icon={<FiTarget className="h-6 w-6 text-white" />} 
            color="bg-purple-500/20"
          />
        </div>
        
        {/* Main dashboard content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Transactions */}
          <Card title="Recent Transactions" className="lg:col-span-2">
            <div className="space-y-4">
              {recentTransactions.map((transaction) => (
                <div 
                  key={transaction.id} 
                  className="flex justify-between items-center p-3 hover:bg-gray-800/50 rounded-lg transition-colors duration-150"
                >
                  <div>
                    <h4 className="font-medium">{transaction.description}</h4>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm text-gray-400">{transaction.date}</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-gray-800">{transaction.category}</span>
                    </div>
                  </div>
                  <div className={`font-mono font-medium ${transaction.amount.startsWith('+') ? 'text-emerald-400' : 'text-red-400'}`}>
                    {transaction.amount}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-800">
              <Link href="/transactions" className="text-emerald-400 flex items-center text-sm hover:text-emerald-300">
                View all transactions
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </Card>
          
          {/* Budget Overview */}
          <Card title="Budget Overview">
            <div className="space-y-4">
              {budgetCategories.map((category) => (
                <div key={category.id} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span>{category.category}</span>
                    <span>${category.spent} of ${category.budget}</span>
                  </div>
                  <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div 
                      className={`h-full ${
                        category.percentage > 90 ? 'bg-red-500' : 
                        category.percentage > 70 ? 'bg-yellow-500' : 
                        'bg-emerald-500'
                      }`}
                      style={{ width: `${category.percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-800">
              <Link href="/budget" className="text-emerald-400 flex items-center text-sm hover:text-emerald-300">
                Manage budget
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>
          </Card>
        </div>
        
        {/* Quick actions */}
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