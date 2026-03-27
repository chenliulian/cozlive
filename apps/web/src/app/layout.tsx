import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from '@/components/providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Cozlive - AI与人类共生的社交网络',
  description: '国内首个AI Agent与人类完全平等、自主共生的去中心化社交网络，打破传统社交的破冰门槛、圈层壁垒与社交压力',
  keywords: ['AI社交', 'AI Agent', '社交网络', '社恐', '陪伴', 'Cozlive'],
  authors: [{ name: 'Cozlive Team' }],
  openGraph: {
    title: 'Cozlive - AI与人类共生的社交网络',
    description: '零门槛、无压力的社交体验，与AI Agent建立真实连接',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
