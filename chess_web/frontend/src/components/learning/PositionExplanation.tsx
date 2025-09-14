import React, { useState } from "react";
import {
  BookOpen,
  Lightbulb,
  Target,
  Shield,
  Crown,
  Zap,
  ChevronDown,
  ChevronRight,
  Info,
  AlertCircle,
  CheckCircle,
} from "lucide-react";
import { cn } from "@utils/index";

interface PositionExplanationProps {
  fen: string;
  explanation?: {
    overview: string;
    keyFeatures: string[];
    strategicConcepts: string[];
    tacticalOpportunities: string[];
    learningPoints: string[];
  };
  loading?: boolean;
  onRequestExplanation: () => void;
}

const PositionExplanation: React.FC<PositionExplanationProps> = ({
  fen,
  explanation,
  loading = false,
  onRequestExplanation,
}) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(["overview"])
  );

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

  const sections = [
    {
      id: "overview",
      title: "Position Overview",
      icon: BookOpen,
      color: "text-blue-600 dark:text-blue-400",
      content: explanation?.overview,
      description: "General assessment of the current position",
    },
    {
      id: "features",
      title: "Key Features",
      icon: Target,
      color: "text-green-600 dark:text-green-400",
      content: explanation?.keyFeatures,
      description: "Important elements that define this position",
    },
    {
      id: "strategic",
      title: "Strategic Concepts",
      icon: Crown,
      color: "text-purple-600 dark:text-purple-400",
      content: explanation?.strategicConcepts,
      description: "Long-term planning and positional ideas",
    },
    {
      id: "tactical",
      title: "Tactical Opportunities",
      icon: Zap,
      color: "text-orange-600 dark:text-orange-400",
      content: explanation?.tacticalOpportunities,
      description: "Immediate tactical possibilities and threats",
    },
    {
      id: "learning",
      title: "Learning Points",
      icon: Lightbulb,
      color: "text-yellow-600 dark:text-yellow-400",
      content: explanation?.learningPoints,
      description: "Key lessons and takeaways from this position",
    },
  ];

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="spinner mx-auto mb-4" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Analyzing position...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!explanation) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="text-center py-12">
          <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400 dark:text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Position Explanation
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Get detailed insights about this chess position including strategic
            concepts, tactical opportunities, and learning points.
          </p>
          <button onClick={onRequestExplanation} className="btn btn-primary">
            <BookOpen className="h-4 w-4 mr-2" />
            Explain Position
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
            <BookOpen className="h-5 w-5 mr-2 text-primary-600" />
            Position Explanation
          </h3>

          <button
            onClick={onRequestExplanation}
            className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            title="Refresh explanation"
          >
            <BookOpen className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 space-y-4">
        {sections.map((section) => {
          const Icon = section.icon;
          const isExpanded = expandedSections.has(section.id);
          const hasContent =
            section.content &&
            (typeof section.content === "string"
              ? section.content.length > 0
              : section.content.length > 0);

          return (
            <div
              key={section.id}
              className="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden"
            >
              {/* Section Header */}
              <button
                onClick={() => toggleSection(section.id)}
                className="w-full p-4 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div
                      className={cn(
                        "p-2 rounded-lg bg-gray-100 dark:bg-gray-700",
                        section.color
                      )}
                    >
                      <Icon className="h-5 w-5" />
                    </div>

                    <div>
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        {section.title}
                      </h4>
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        {section.description}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    {hasContent && (
                      <div className="flex items-center space-x-1">
                        <CheckCircle className="h-4 w-4 text-green-500" />
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {typeof section.content === "string"
                            ? "1 item"
                            : `${section.content.length} items`}
                        </span>
                      </div>
                    )}

                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4 text-gray-400" />
                    ) : (
                      <ChevronRight className="h-4 w-4 text-gray-400" />
                    )}
                  </div>
                </div>
              </button>

              {/* Section Content */}
              {isExpanded && (
                <div className="px-4 pb-4 border-t border-gray-200 dark:border-gray-700">
                  {hasContent ? (
                    <div className="pt-4">
                      {typeof section.content === "string" ? (
                        <div className="prose prose-sm dark:prose-invert max-w-none">
                          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                            {section.content}
                          </p>
                        </div>
                      ) : (
                        <ul className="space-y-2">
                          {section.content.map((item, index) => (
                            <li
                              key={index}
                              className="flex items-start space-x-3 text-sm text-gray-700 dark:text-gray-300"
                            >
                              <div className="flex-shrink-0 w-2 h-2 bg-primary-500 rounded-full mt-2" />
                              <span className="leading-relaxed">{item}</span>
                            </li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ) : (
                    <div className="pt-4 text-center">
                      <Info className="h-8 w-8 mx-auto mb-2 text-gray-400 dark:text-gray-600" />
                      <p className="text-sm text-gray-500 dark:text-gray-400">
                        No {section.title.toLowerCase()} available for this
                        position
                      </p>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Footer with tips */}
      <div className="p-6 bg-gray-50 dark:bg-gray-700 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-start space-x-3">
          <Lightbulb className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
          <div>
            <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-1">
              💡 Study Tips
            </h5>
            <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
              <li>
                • Focus on understanding the key features before looking for
                tactics
              </li>
              <li>
                • Consider both short-term tactics and long-term strategic plans
              </li>
              <li>• Practice identifying similar patterns in your own games</li>
              <li>
                • Use the learning points to improve your general chess
                understanding
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PositionExplanation;
