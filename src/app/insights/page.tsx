"use client";

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { motion } from 'framer-motion';
import { redirect } from 'next/navigation';
import Link from 'next/link';
import { FiChevronLeft, FiSearch, FiRefreshCw, FiInfo, FiTrendingUp, FiTrendingDown, FiAlertCircle } from 'react-icons/fi';

// Insight Card Component
const InsightCard = ({ insight }: { 
  insight: { 
    id: number, 
    title: string, 
    content: string, 
    category: string, 
    date: string,
    type: 'positive' | 'negative' | 'neutral' | 'alert'
  }
}) => {
  const [expanded, setExpanded] = useState(false);
  
  // Select icon based on type
  const getIcon = () => {
    switch (insight.type) {
      case 'positive':
        return <FiTrendingUp className="h-5 w-5 text-emerald-400" />;
      case 'negative':
        return <FiTrendingDown className="h-5 w-5 text-red-400" />;
      case 'alert':
        return <FiAlertCircle className="h-5 w-5 text-yellow-400" />;
      default:
        return <FiInfo className="h-5 w-5 text-blue-400" />;
    }
  };
  
  // Select background color based on type
  const getColor = () => {
    switch (insight.type) {
      case 'positive':
        return 'border-emerald-500/20 bg-gradient-to-br from-gray-900 to-emerald-900/10';
      case 'negative':
        return 'border-red-500/20 bg-gradient-to-br from-gray-900 to-red-900/10';
      case 'alert':
        return 'border-yellow-500/20 bg-gradient-to-br from-gray-900 to-yellow-900/10';
      default:
        return 'border-blue-500/20 bg-gradient-to-br from-gray-900 to-blue-900/10';
    }
  };
  
  return (
    <motion.div 
      className={`p-4 rounded-xl border ${getColor()} hover:shadow-lg transition-all duration-300`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-start space-x-3">
        <div className="mt-1">
          {getIcon()}
        </div>
        <div className="flex-1">
          <h3 className="font-medium text-lg mb-2">{insight.title}</h3>
          <div className={`overflow-hidden transition-all duration-300 ${expanded ? 'max-h-96' : 'max-h-16'}`}>
            <p className="text-gray-300 text-sm">
              {insight.content}
            </p>
          </div>
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center space-x-2">
              <span className="text-xs px-2 py-1 rounded-full bg-gray-800">{insight.category}</span>
              <span className="text-xs text-gray-400">{insight.date}</span>
            </div>
            <button 
              onClick={() => setExpanded(!expanded)} 
              className="text-xs text-emerald-400 hover:text-emerald-300"
            >
              {expanded ? 'Show less' : 'Read more'}
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default function InsightsPage() {
  const { isLoaded, isSignedIn } = useUser();
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  // Sample insights data
  const insightsData = [
    { 
      id: 1, 
      title: "Unusual spending pattern detected", 
      content: "We've noticed your spending in the 'Entertainment' category has increased by 45% compared to your monthly average. This might be affecting your ability to meet your savings goal for this month. Consider reviewing your recent entertainment expenses and look for opportunities to reduce discretionary spending.",
      category: "Spending Patterns", 
      date: "Today",
      type: 'alert'
    },
    { 
      id: 2, 
      title: "Saving opportunity identified", 
      content: "Based on your subscription expenses, you have 3 streaming services totaling $42.97 monthly. Our analysis shows low usage for Netflix ($15.99/mo) in the past 60 days. Consider pausing or canceling this subscription to save approximately $192 annually.",
      category: "Savings Opportunity", 
      date: "Yesterday",
      type: 'positive'
    },
    { 
      id: 3, 
      title: "Budget optimization recommendation", 
      content: "Your current allocation to the 'Food' category (30% of your budget) is higher than the recommended level (15-20%). Based on your historical spending patterns and financial goals, we recommend reducing your food budget by 5-10% and redirecting those funds to your emergency savings, which is currently below the recommended 3-month expense coverage.",
      category: "Budget", 
      date: "Oct 8, 2023",
      type: 'neutral'
    },
    { 
      id: 4, 
      title: "Monthly expense trend analysis", 
      content: "Your utility bills have increased by 18% compared to the same period last year. This trend is higher than the average inflation rate of 3.2%. We recommend checking for potential leaks, reviewing your energy consumption patterns, or exploring more competitive utility providers to mitigate this increase.",
      category: "Expense Trends", 
      date: "Oct 5, 2023",
      type: 'negative'
    },
    { 
      id: 5, 
      title: "Investment portfolio diversification", 
      content: "Your investment portfolio is currently weighted 85% in technology stocks, which exposes you to significant sector risk. Based on your risk profile and financial goals, we recommend diversifying your investments across multiple sectors and asset classes. Consider allocating 15-20% of your portfolio to defensive sectors like consumer staples and utilities to reduce volatility.",
      category: "Investments", 
      date: "Oct 2, 2023",
      type: 'neutral'
    },
    { 
      id: 6, 
      title: "Savings goal progress update", 
      content: "Congratulations! You've reached 75% of your 'Home Down Payment' savings goal. At your current savings rate, you'll achieve your target of $60,000 in approximately 8 months, which is 2 months ahead of your original timeline. Keep up the great work and consider increasing your savings rate to achieve your goal even sooner.",
      category: "Goals", 
      date: "Sep 28, 2023",
      type: 'positive'
    },
  ];

  // Filter categories
  const categories = [
    { id: 'all', name: 'All Insights' },
    { id: 'spending', name: 'Spending Patterns' },
    { id: 'savings', name: 'Savings Opportunities' },
    { id: 'budget', name: 'Budget' },
    { id: 'trends', name: 'Expense Trends' },
    { id: 'investments', name: 'Investments' },
    { id: 'goals', name: 'Goals' },
  ];

  // Filter insights
  const filteredInsights = insightsData
    .filter(insight => {
      if (filter === 'all') return true;
      return insight.category.toLowerCase().includes(filter.toLowerCase());
    })
    .filter(insight => {
      if (!searchTerm) return true;
      return (
        insight.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        insight.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
        insight.category.toLowerCase().includes(searchTerm.toLowerCase())
      );
    });

  // Generate new insights
  const handleGenerateInsights = () => {
    setIsGenerating(true);
    // Simulating API call
    setTimeout(() => {
      setIsGenerating(false);
      // Logic to generate and add new insights would go here
    }, 2000);
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
                  AI Financial Insights
                </span>
              </h1>
            </div>
            <button
              onClick={handleGenerateInsights}
              disabled={isGenerating}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
                isGenerating 
                  ? 'bg-gray-800 text-gray-400 cursor-not-allowed' 
                  : 'bg-emerald-600 hover:bg-emerald-700 text-white'
              } transition-colors`}
            >
              <FiRefreshCw className={`h-4 w-4 ${isGenerating ? 'animate-spin' : ''}`} />
              <span>{isGenerating ? 'Generating...' : 'Generate New Insights'}</span>
            </button>
          </div>
        </div>
      </header>
      
      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters and search */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-8">
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setFilter(category.id)}
                className={`px-3 py-1.5 text-sm rounded-full transition-colors ${
                  filter === category.id
                    ? 'bg-emerald-600 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
          
          <div className="relative w-full md:w-64">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <FiSearch className="h-5 w-5 text-gray-400" />
            </div>
            <input 
              type="text" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search insights..." 
              className="bg-gray-900/60 border border-gray-800 w-full pl-10 pr-4 py-2 rounded-lg text-gray-300 
                       focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
            />
          </div>
        </div>
        
        {/* Insights list */}
        <div className="space-y-6">
          {filteredInsights.length > 0 ? (
            filteredInsights.map((insight) => (
              <InsightCard key={insight.id} insight={insight} />
            ))
          ) : (
            <div className="bg-gray-900/40 rounded-xl border border-gray-800 p-8 text-center">
              <p className="text-gray-400">No insights found. Try a different filter or generate new insights.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}