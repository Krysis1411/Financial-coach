import type { Metadata } from "next";

import { AppProviders } from "@/components/app-providers";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";

export const metadata: Metadata = {
  title: "AI Financial Coach",
  description:
    "A multi-agent AI financial coach: budget analysis, savings strategy, and debt-payoff plans rendered as interactive cards. Built with Google ADK + CopilotKit + AG-UI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
