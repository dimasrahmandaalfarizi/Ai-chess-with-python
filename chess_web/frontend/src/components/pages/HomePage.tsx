import React from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Play,
  BarChart3,
  Puzzle,
  BookOpen,
  Crown,
  Zap,
  Target,
  Brain,
  ArrowRight,
  Star,
  Users,
  TrendingUp,
} from "lucide-react";
import { motion } from "framer-motion";

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description:
        "Get deep insights into your positions with advanced chess engine analysis",
      color: "text-blue-600 dark:text-blue-400",
    },
    {
      icon: Target,
      title: "Tactical Training",
      description:
        "Improve your tactical skills with thousands of puzzles and exercises",
      color: "text-green-600 dark:text-green-400",
    },
    {
      icon: BookOpen,
      title: "Interactive Lessons",
      description:
        "Learn chess concepts with guided lessons and practical examples",
      color: "text-purple-600 dark:text-purple-400",
    },
    {
      icon: TrendingUp,
      title: "Progress Tracking",
      description:
        "Monitor your improvement with detailed statistics and analytics",
      color: "text-orange-600 dark:text-orange-400",
    },
  ];

  const stats = [
    { label: "Active Players", value: "10,000+", icon: Users },
    { label: "Puzzles Solved", value: "1M+", icon: Puzzle },
    { label: "Games Analyzed", value: "500K+", icon: BarChart3 },
    { label: "Average Rating", value: "1,247", icon: Star },
  ];

  const quickActions = [
    {
      title: "Play vs AI",
      description: "Start a game against our intelligent chess engine",
      icon: Play,
      href: "/game",
      color: "bg-green-600 hover:bg-green-700",
      primary: true,
    },
    {
      title: "Analyze Position",
      description: "Get deep analysis of any chess position",
      icon: BarChart3,
      href: "/analysis",
      color: "bg-blue-600 hover:bg-blue-700",
    },
    {
      title: "Solve Puzzles",
      description: "Improve your tactics with daily puzzles",
      icon: Puzzle,
      href: "/puzzles",
      color: "bg-purple-600 hover:bg-purple-700",
    },
    {
      title: "Learn Chess",
      description: "Master chess with interactive lessons",
      icon: BookOpen,
      href: "/learn",
      color: "bg-orange-600 hover:bg-orange-700",
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative py-20 lg:py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50 to-blue-50 dark:from-gray-900 dark:to-gray-800"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="flex justify-center mb-8"
            >
              <Crown className="h-16 w-16 text-primary-600" />
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6"
            >
              Master Chess with{" "}
              <span className="text-primary-600">AI Intelligence</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto"
            >
              Elevate your chess game with advanced AI analysis, personalized
              training, and interactive lessons. From beginner to grandmaster,
              we'll help you improve.
            </motion.p>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <button
                onClick={() => navigate("/game")}
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
              >
                <Play className="mr-2 h-5 w-5" />
                Start Playing
              </button>
              <button
                onClick={() => navigate("/analysis")}
                className="inline-flex items-center px-8 py-4 border border-gray-300 dark:border-gray-600 text-lg font-medium rounded-lg text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
              >
                <BarChart3 className="mr-2 h-5 w-5" />
                Analyze Position
              </button>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <Icon className="h-8 w-8 text-primary-600 mx-auto mb-4" />
                  <div className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              What would you like to do?
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Choose your path to chess improvement
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickActions.map((action, index) => {
              const Icon = action.icon;
              return (
                <motion.div
                  key={action.title}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                >
                  <Link
                    to={action.href}
                    className={`block p-6 rounded-xl text-white ${action.color} transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl`}
                  >
                    <Icon className="h-8 w-8 mb-4" />
                    <h3 className="text-xl font-semibold mb-2">
                      {action.title}
                    </h3>
                    <p className="text-sm opacity-90">{action.description}</p>
                    <ArrowRight className="h-5 w-5 mt-4 opacity-75" />
                  </Link>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Powerful Features for Every Player
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Everything you need to improve your chess game
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="flex items-start space-x-4 p-6 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  <div
                    className={`flex-shrink-0 p-3 rounded-lg bg-gray-100 dark:bg-gray-700`}
                  >
                    <Icon className={`h-6 w-6 ${feature.color}`} />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300">
                      {feature.description}
                    </p>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-primary-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Improve Your Chess?
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Join thousands of players who are already improving their game
            </p>
            <button
              onClick={() => navigate("/game")}
              className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-primary-600 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              <Zap className="mr-2 h-5 w-5" />
              Get Started Now
            </button>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
