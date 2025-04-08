"use client";

import * as React from "react";
import { ThemeProvider as NextThemesProvider } from "next-themes";

// Simple wrapper component that ignores type issues temporarily
export function ThemeProvider({ 
  children,
  ...props
}: { 
  children: React.ReactNode;
  attribute?: string;
  defaultTheme?: string;
  enableSystem?: boolean;
}) {
  // @ts-ignore - Ignoring type issues temporarily to get the app running
  return <NextThemesProvider {...props}>{children}</NextThemesProvider>;
}