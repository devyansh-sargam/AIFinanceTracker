export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-6 md:p-24 bg-black text-white">
      <h1 className="text-4xl md:text-6xl font-bold mb-6">
        <span className="bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-teal-600">
          AI Finance Assistant
        </span>
      </h1>
      
      <p className="text-lg md:text-xl text-gray-300 mb-8 mx-auto max-w-2xl text-center">
        Take control of your finances with AI-powered insights, personalized recommendations, 
        and intelligent budget planning to achieve your financial goals.
      </p>
      
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <button className="bg-gradient-to-r from-emerald-500 to-teal-600 
                  text-white font-bold py-3 px-8 rounded-lg shadow-lg">
          Get Started
        </button>
        
        <button className="bg-gray-800 text-white font-bold py-3 px-8 rounded-lg 
                  shadow-lg border border-gray-700">
          Sign In
        </button>
      </div>
      
      <footer className="mt-16 text-gray-500 text-center">
        <p>&copy; {new Date().getFullYear()} AI Finance Assistant. All rights reserved.</p>
      </footer>
    </main>
  );
}