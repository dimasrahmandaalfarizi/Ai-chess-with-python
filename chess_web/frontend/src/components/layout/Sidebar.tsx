import React from "react";
import { Link, useLocation } from "react-router-dom";
import {
  Home,
  Play,
  BarChart3,
  Puzzle,
  BookOpen,
  Settings,
  Trophy,
  Clock,
  Target,
  Brain,
} from "lucide-react";
import { cn } from "@utils/index";

interface SidebarProps {
  className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({ className }) => {
  const location = useLocation();

  const navigation = [
    {
      name: "Dashboard",
      href: "/",
      icon: Home,
      current: location.pathname === "/",
      description: "Overview and statistics",
    },
    {
      name: "Play Game",
      href: "/game",
      icon: Play,
      current: location.pathname.startsWith("/game"),
      description: "Play against AI",
    },
    {
      name: "Analysis",
      href: "/analysis",
      icon: BarChart3,
      current: location.pathname === "/analysis",
      description: "Analyze positions",
    },
    {
      name: "Puzzles",
      href: "/puzzles",
      icon: Puzzle,
      current: location.pathname === "/puzzles",
      description: "Tactical training",
    },
    {
      name: "Learn",
      href: "/learn",
      icon: BookOpen,
      current: location.pathname === "/learn",
      description: "Chess lessons",
    },
  ];

  const quickActions = [
    {
      name: "Quick Game",
      href: "/game?quick=true",
      icon: Clock,
      color: "text-green-600 dark:text-green-400",
    },
    {
      name: "Daily Puzzle",
      href: "/puzzles/daily",
      icon: Target,
      color: "text-blue-600 dark:text-blue-400",
    },
    {
      name: "Training",
      href: "/learn/training",
      icon: Brain,
      color: "text-purple-600 dark:text-purple-400",
    },
    {
      name: "Tournaments",
      href: "/tournaments",
      icon: Trophy,
      color: "text-yellow-600 dark:text-yellow-400",
    },
  ];

  return (
    <div
      className={cn(
        "fixed inset-y-0 left-0 z-40 w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 pt-16",
        className
      )}
    >
      <div className="flex flex-col h-full">
        {/* Main Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2">
          <div className="mb-6">
            <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Main Menu
            </h3>
          </div>

          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  item.current
                    ? "bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300"
                    : "text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700"
                )}
              >
                <Icon
                  className={cn(
                    "mr-3 h-5 w-5 flex-shrink-0",
                    item.current
                      ? "text-primary-600 dark:text-primary-400"
                      : "text-gray-400 dark:text-gray-500 group-hover:text-primary-500"
                  )}
                />
                <div className="flex-1">
                  <div>{item.name}</div>
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    {item.description}
                  </div>
                </div>
              </Link>
            );
          })}
        </nav>

        {/* Quick Actions */}
        <div className="px-4 py-6 border-t border-gray-200 dark:border-gray-700">
          <div className="mb-4">
            <h3 className="px-3 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Quick Actions
            </h3>
          </div>

          <div className="space-y-2">
            {quickActions.map((action) => {
              const Icon = action.icon;
              return (
                <Link
                  key={action.name}
                  to={action.href}
                  className="group flex items-center px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <Icon
                    className={cn("mr-3 h-4 w-4 flex-shrink-0", action.color)}
                  />
                  {action.name}
                </Link>
              );
            })}
          </div>
        </div>

        {/* Settings */}
        <div className="px-4 py-4 border-t border-gray-200 dark:border-gray-700">
          <Link
            to="/settings"
            className={cn(
              "group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
              location.pathname === "/settings"
                ? "bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300"
                : "text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            )}
          >
            <Settings
              className={cn(
                "mr-3 h-5 w-5 flex-shrink-0",
                location.pathname === "/settings"
                  ? "text-primary-600 dark:text-primary-400"
                  : "text-gray-400 dark:text-gray-500 group-hover:text-primary-500"
              )}
            />
            Settings
          </Link>
        </div>

        {/* User Stats */}
        <div className="px-4 py-4 bg-gray-50 dark:bg-gray-900">
          <div className="text-xs text-gray-500 dark:text-gray-400 mb-2">
            Your Progress
          </div>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Rating</span>
              <span className="font-medium text-gray-900 dark:text-gray-100">
                1247
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Puzzles</span>
              <span className="font-medium text-gray-900 dark:text-gray-100">
                156
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-400">Games</span>
              <span className="font-medium text-gray-900 dark:text-gray-100">
                42
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
