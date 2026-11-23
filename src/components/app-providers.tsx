"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { useEffect, useState } from "react";

const USER_ID_STORAGE_KEY = "financial-coach-user-id";

function getOrCreateUserId(): string {
  try {
    const existing = window.localStorage.getItem(USER_ID_STORAGE_KEY);
    if (existing) return existing;
    const created = crypto.randomUUID();
    window.localStorage.setItem(USER_ID_STORAGE_KEY, created);
    return created;
  } catch {
    return crypto.randomUUID();
  }
}

export function AppProviders({ children }: { children: React.ReactNode }) {
  const [userId, setUserId] = useState<string | null>(null);

  useEffect(() => {
    setUserId(getOrCreateUserId());
  }, []);

  if (!userId) return null;

  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
      agent="my_agent"
      properties={{ userId }}
    >
      {children}
    </CopilotKit>
  );
}
