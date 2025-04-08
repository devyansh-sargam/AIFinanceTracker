// This file is temporarily disabled due to compatibility issues with Clerk
// We will enable it later once the issues are fixed

export const config = {
  matcher: [], // No routes are matched by the middleware for now
};

// This is a workaround until we fix the middleware
export default function middleware() {
  return;
}