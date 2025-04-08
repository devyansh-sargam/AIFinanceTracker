import OpenAI from 'openai';

// Check if the OPENAI_API_KEY is available in the environment
if (!process.env.OPENAI_API_KEY) {
  console.warn('Missing OPENAI_API_KEY environment variable');
}

// Create an OpenAI API client
export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function generateFinancialInsight(data: any) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o", // the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
      messages: [
        {
          role: "system",
          content: `You are a financial advisor. Analyze the following financial data and provide 
          personalized insights, recommendations for improvement, and actionable steps to achieve 
          better financial health. Focus on patterns, potential savings, and optimizations.`,
        },
        {
          role: "user",
          content: `Here is my financial data: ${JSON.stringify(data)}`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    return response.choices[0].message.content;
  } catch (error) {
    console.error('Error generating financial insight:', error);
    throw new Error('Failed to generate financial insights. Please try again later.');
  }
}

export async function generateBudgetRecommendation(income: number, expenses: any[]) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o", // the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
      messages: [
        {
          role: "system",
          content: `You are a budget optimization expert. Create a recommended budget allocation 
          based on the provided income and current expenses. Use the 50/30/20 rule as a baseline 
          (50% needs, 30% wants, 20% savings), but adjust based on the user's specific situation.`,
        },
        {
          role: "user",
          content: `My monthly income is $${income} and my expenses are: ${JSON.stringify(expenses)}. 
          Please recommend a budget.`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
      response_format: { type: "json_object" },
    });

    return JSON.parse(response.choices[0].message.content || '{}');
  } catch (error) {
    console.error('Error generating budget recommendation:', error);
    throw new Error('Failed to generate budget recommendation. Please try again later.');
  }
}

export async function analyzeSpendingTrends(expenses: any[], period: string) {
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4o", // the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
      messages: [
        {
          role: "system",
          content: `You are a spending pattern analyst. Examine the provided expenses data 
          and identify key trends, unusual spending patterns, and potential areas for saving money.
          Provide insights in a clear, concise format with actionable recommendations.`,
        },
        {
          role: "user",
          content: `Here are my expenses for the ${period} period: ${JSON.stringify(expenses)}. 
          Please analyze my spending trends.`,
        },
      ],
      temperature: 0.7,
      max_tokens: 1000,
    });

    return response.choices[0].message.content;
  } catch (error) {
    console.error('Error analyzing spending trends:', error);
    throw new Error('Failed to analyze spending trends. Please try again later.');
  }
}