import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  basePath: '/study-assistant',
  async rewrites() {
    return [
      {
        source: "/api/:path*", // Intercetta le chiamate API
        destination: "http://127.0.0.1:8000/api/:path*", // Proxy locale a FastAPI
      },
    ];
  },
};

export default nextConfig;
