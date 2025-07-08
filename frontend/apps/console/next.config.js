/** @type {import('next').NextConfig} */
const nextConfig = {
  redirects: async () => [
    {
      source: '/',
      destination: '/app/projects',
      permanent: false,
    },
    {
      source: '/app',
      destination: '/app/projects',
      permanent: false,
    },
    ],
  };

export default nextConfig;
