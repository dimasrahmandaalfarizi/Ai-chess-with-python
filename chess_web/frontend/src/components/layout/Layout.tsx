import React from "react";
import { useLocation } from "react-router-dom";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";
import { useThemeStore } from "@store/themeStore";
import { cn } from "@utils/index";

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();
  const { isDarkMode } = useThemeStore();

  // Determine if sidebar should be shown
  const showSidebar = !location.pathname.includes("/game/");

  // Determine layout classes based on page
  const isFullscreen =
    location.pathname.includes("/game/") || location.pathname === "/analysis";

  return (
    <div
      className={cn(
        "min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200",
        isDarkMode && "dark"
      )}
    >
      {/* Header */}
      <Header />

      <div className="flex">
        {/* Sidebar */}
        {showSidebar && <Sidebar className="hidden lg:block" />}

        {/* Main Content */}
        <main
          className={cn(
            "flex-1 transition-all duration-200",
            showSidebar ? "lg:ml-64" : "",
            isFullscreen ? "pt-16" : "pt-16 pb-16"
          )}
        >
          <div
            className={cn(
              "container mx-auto",
              isFullscreen
                ? "max-w-none px-4"
                : "max-w-7xl px-4 sm:px-6 lg:px-8"
            )}
          >
            {children}
          </div>
        </main>
      </div>

      {/* Footer */}
      {!isFullscreen && <Footer />}
    </div>
  );
};

export default Layout;
