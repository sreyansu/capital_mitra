import { ArrowRight, Zap, Clock, Lock, TrendingUp, FileText, CheckCircle2 } from 'lucide-react';

interface LandingPageProps {
  onGetStarted: () => void;
}

export default function LandingPage({ onGetStarted }: LandingPageProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 sticky top-0 z-40 bg-black bg-opacity-80 backdrop-blur">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">CM</span>
            </div>
            <h1 className="text-xl font-semibold">CapitalMitra</h1>
          </div>
          <button
            onClick={onGetStarted}
            className="bg-orange-600 hover:bg-orange-700 px-6 py-2 rounded-lg font-semibold transition-all shadow-lg hover:shadow-xl"
          >
            Get Started
          </button>
        </div>
      </nav>

      <main>
        <section className="max-w-7xl mx-auto px-6 py-20 md:py-32">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div className="space-y-8 animate-fadeIn">
              <div>
                <h2 className="text-5xl md:text-6xl font-bold leading-tight mb-4">
                  Your Personal Loan,
                  <span className="text-orange-600"> In Minutes</span>
                </h2>
                <p className="text-xl text-gray-400">
                  From inquiry to sanction letter through an intelligent AI conversation. Fast, transparent, and hassle-free.
                </p>
              </div>

              <div className="flex flex-col sm:flex-row gap-4">
                <button
                  onClick={onGetStarted}
                  className="bg-orange-600 hover:bg-orange-700 px-8 py-4 rounded-xl font-semibold text-lg transition-all shadow-lg hover:shadow-2xl flex items-center justify-center space-x-2"
                >
                  <span>Start Your Journey</span>
                  <ArrowRight size={20} />
                </button>
                <button className="border border-gray-600 hover:border-orange-600 px-8 py-4 rounded-xl font-semibold text-lg transition-all hover:bg-gray-800">
                  Learn More
                </button>
              </div>

              <div className="flex items-center space-x-6 text-sm text-gray-400">
                <div className="flex items-center space-x-2">
                  <CheckCircle2 size={18} className="text-orange-600" />
                  <span>100% Secure</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle2 size={18} className="text-orange-600" />
                  <span>No Hidden Fees</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle2 size={18} className="text-orange-600" />
                  <span>Instant Approval</span>
                </div>
              </div>
            </div>

            <div className="relative hidden md:block">
              <div className="absolute inset-0 bg-gradient-to-r from-orange-600 to-orange-400 rounded-2xl blur-3xl opacity-20"></div>
              <div className="relative bg-gray-800 rounded-2xl p-8 border border-gray-700 shadow-2xl">
                <div className="space-y-4">
                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 bg-orange-600 rounded-full flex-shrink-0"></div>
                    <div className="flex-1 space-y-2">
                      <p className="text-sm text-gray-400">CapitalMitra AI</p>
                      <p className="text-white">Hello! Tell me about your loan needs and we'll find the perfect offer for you.</p>
                    </div>
                  </div>

                  <div className="flex justify-end">
                    <div className="bg-orange-600 rounded-2xl rounded-tr-none px-4 py-3 max-w-xs">
                      <p className="text-sm">I need ₹5 lakhs for my wedding</p>
                    </div>
                  </div>

                  <div className="flex items-start space-x-4">
                    <div className="w-10 h-10 bg-orange-600 rounded-full flex-shrink-0"></div>
                    <div className="flex-1 space-y-2">
                      <p className="text-sm text-gray-400">CapitalMitra AI</p>
                      <p className="text-white">Great! You're pre-approved for ₹8L at 10.5% interest. Ready to proceed?</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="bg-gray-800 bg-opacity-50 border-y border-gray-700 py-16 md:py-20">
          <div className="max-w-7xl mx-auto px-6">
            <h3 className="text-3xl font-bold mb-12 text-center">How It Works</h3>
            <div className="grid md:grid-cols-4 gap-8">
              {[
                {
                  icon: Zap,
                  title: 'Chat',
                  description: 'Share your loan needs with our AI assistant'
                },
                {
                  icon: TrendingUp,
                  title: 'Get Offer',
                  description: 'Receive pre-approved loan offers instantly'
                },
                {
                  icon: FileText,
                  title: 'Verify',
                  description: 'Quick KYC and document verification'
                },
                {
                  icon: CheckCircle2,
                  title: 'Approve',
                  description: 'Get your sanction letter in minutes'
                }
              ].map((step, index) => {
                const Icon = step.icon;
                return (
                  <div key={index} className="relative">
                    <div className="bg-gray-900 rounded-xl p-6 text-center">
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-orange-600 bg-opacity-20 rounded-full mb-4">
                        <Icon size={32} className="text-orange-600" />
                      </div>
                      <h4 className="text-xl font-semibold mb-2">{step.title}</h4>
                      <p className="text-gray-400 text-sm">{step.description}</p>
                    </div>
                    {index < 3 && (
                      <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                        <ArrowRight size={24} className="text-orange-600" />
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        <section className="max-w-7xl mx-auto px-6 py-16 md:py-20">
          <h3 className="text-3xl font-bold mb-12 text-center">Why Choose CapitalMitra?</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Clock,
                title: 'Lightning Fast',
                description: 'Get sanctioned in under 10 minutes. No waiting, no delays.'
              },
              {
                icon: Lock,
                title: 'Completely Secure',
                description: 'Bank-grade encryption protects your data every step of the way.'
              },
              {
                icon: TrendingUp,
                title: 'Competitive Rates',
                description: 'Get the best interest rates tailored to your credit profile.'
              },
              {
                icon: FileText,
                title: 'Transparent Process',
                description: 'No hidden fees. Know exactly what you\'re getting into.'
              },
              {
                icon: Zap,
                title: 'AI-Powered Support',
                description: 'Instant responses to all your questions. Available 24/7.'
              },
              {
                icon: CheckCircle2,
                title: 'Instant Approval',
                description: 'Real-time credit assessment with immediate decision.'
              }
            ].map((feature, index) => {
              const Icon = feature.icon;
              return (
                <div key={index} className="bg-gray-800 bg-opacity-50 rounded-xl p-6 border border-gray-700 hover:border-orange-600 transition-all hover:shadow-lg">
                  <Icon size={32} className="text-orange-600 mb-4" />
                  <h4 className="text-lg font-semibold mb-2">{feature.title}</h4>
                  <p className="text-gray-400 text-sm">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </section>

        <section className="bg-gradient-to-r from-orange-600 to-orange-700 py-16 md:py-20">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <h3 className="text-4xl font-bold mb-6">Ready to Get Your Loan?</h3>
            <p className="text-xl mb-8 text-orange-50">
              Join thousands of satisfied customers who got their loans approved in minutes.
            </p>
            <button
              onClick={onGetStarted}
              className="bg-white text-orange-600 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg transition-all shadow-lg hover:shadow-xl"
            >
              Start Your Application Now
            </button>
          </div>
        </section>

        <footer className="border-t border-gray-800 py-12">
          <div className="max-w-7xl mx-auto px-6">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <h5 className="font-semibold mb-4">CapitalMitra</h5>
                <p className="text-gray-400 text-sm">Your AI-powered personal loan assistant.</p>
              </div>
              <div>
                <h5 className="font-semibold mb-4">Product</h5>
                <ul className="text-gray-400 text-sm space-y-2">
                  <li><a href="#" className="hover:text-orange-600 transition">Features</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">Pricing</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">FAQ</a></li>
                </ul>
              </div>
              <div>
                <h5 className="font-semibold mb-4">Company</h5>
                <ul className="text-gray-400 text-sm space-y-2">
                  <li><a href="#" className="hover:text-orange-600 transition">About</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">Blog</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">Careers</a></li>
                </ul>
              </div>
              <div>
                <h5 className="font-semibold mb-4">Legal</h5>
                <ul className="text-gray-400 text-sm space-y-2">
                  <li><a href="#" className="hover:text-orange-600 transition">Privacy</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">Terms</a></li>
                  <li><a href="#" className="hover:text-orange-600 transition">Contact</a></li>
                </ul>
              </div>
            </div>
            <div className="border-t border-gray-800 pt-8 text-center text-gray-400 text-sm">
              <p>&copy; 2024 CapitalMitra. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </main>
    </div>
  );
}
