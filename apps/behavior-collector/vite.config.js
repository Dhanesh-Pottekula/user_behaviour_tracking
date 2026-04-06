import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // Allow dev-tunnel hosts like ngrok without editing this file each time the URL changes.
    allowedHosts: true,
    port: 5174,
  },
});
