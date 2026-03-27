import { Hero } from '@/components/layout/hero';
import { AgentShowcase } from '@/components/agent/agent-showcase';
import { Features } from '@/components/layout/features';
import { HowItWorks } from '@/components/layout/how-it-works';
import { CTASection } from '@/components/layout/cta-section';
import { MainLayout } from '@/components/layout/main-layout';

export default function Home() {
  return (
    <MainLayout>
      <Hero />
      <AgentShowcase />
      <Features />
      <HowItWorks />
      <CTASection />
    </MainLayout>
  );
}
