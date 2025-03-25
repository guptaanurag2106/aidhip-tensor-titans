import React from 'react'


// Get sentiment color based on value
const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.3) return "text-green-600";
    if (sentiment >= -0.3) return "text-amber-600";
    return "text-red-600";
};

// Get sentiment label based on value
const getSentimentLabel = (sentiment: number) => {
    if (sentiment >= 0.7) return "Very Positive";
    if (sentiment >= 0.3) return "Positive";
    if (sentiment >= -0.3) return "Neutral";
    if (sentiment >= -0.7) return "Negative";
    return "Very Negative";
};

interface SentimentProps {
    sentiment: number
}

const Sentiment = ({ sentiment }: SentimentProps) => {
    return (
        <div
            className={`flex items-center text-xs group ${getSentimentColor(
                sentiment
            )}`}
        >
            Sentiment: {getSentimentLabel(sentiment)}
            <span className="hidden group-hover:inline">
                ({sentiment})
            </span>
        </div>
    )
}

export default Sentiment