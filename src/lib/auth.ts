import { clerkClient } from '@clerk/nextjs';
import { prisma } from './prisma';

// Function to ensure user exists in our database
export async function ensureUserInDatabase(clerkId: string, email: string, name: string | null) {
  try {
    // Check if user exists in our database
    let user = await prisma.user.findUnique({
      where: { clerkId },
    });

    // If user doesn't exist, create a new one
    if (!user) {
      user = await prisma.user.create({
        data: {
          clerkId,
          email,
          name,
        },
      });
      console.log(`Created new user with ID: ${user.id}`);
    }

    return user;
  } catch (error) {
    console.error('Error ensuring user in database:', error);
    throw new Error('Failed to process user data');
  }
}

// Function to get user profile information
export async function getUserProfile(clerkId: string) {
  try {
    // Get user from our database
    const user = await prisma.user.findUnique({
      where: { clerkId },
      include: {
        _count: {
          select: {
            expenses: true,
            incomes: true,
            budgets: true,
            financialGoals: true,
          },
        },
      },
    });

    if (!user) {
      throw new Error('User not found');
    }

    return user;
  } catch (error) {
    console.error('Error getting user profile:', error);
    throw new Error('Failed to retrieve user profile');
  }
}