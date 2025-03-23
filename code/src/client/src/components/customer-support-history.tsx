"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle2, RepeatIcon } from "lucide-react"
import { useCustomerSupportHistory } from "@/lib/api"

// Updated mock support data
const MOCK_SUPPORT = {
  CUST_1: [
    {
      complaint_id: "SPRT_1",
      customer_id: "CUST_1",
      date: "18/08/2023",
      transcript:
        "Hi, I'm calling because I was double-charged for a purchase at Trader Joe's on August 15th. The transaction shows up twice on my online statement, both for $78.52. I checked with Trader Joe's, and they confirmed they only processed one transaction. I'd like to get the duplicate charge removed, please. This is frustrating. My account number is [redacted for privacy].",
      main_concerns: "Billing issue",
      is_repeating_issue: false,
      was_issue_resolved: true,
      sentiment: -0.4,
    },
    {
      complaint_id: "SPRT_2",
      customer_id: "CUST_1",
      date: "05/03/2024",
      transcript:
        "I'm having trouble setting up automatic payments for my credit card through the mobile app. Every time I try to link my checking account, I get an error message that says 'Unable to connect. Please try again later.' I've tried multiple times over the last two days, and it's still not working. The app is fully updated. Is there a known issue, or can you help me resolve this? It is important to pay through my prefered method.",
      main_concerns: "Technical support",
      is_repeating_issue: true,
      was_issue_resolved: false,
      sentiment: -0.6,
    },
  ],
  CUST_2: [
    {
      complaint_id: "SPRT_3",
      customer_id: "CUST_2",
      date: "15/08/2023",
      transcript:
        "I'm calling to dispute a $75 overdraft fee. My account balance was positive when I made the purchase, but the charge posted later, causing the overdraft. It seems like there was a delay in processing, and now I'm being penalized. This isn't fair, as I'm always careful with my budgeting, with a family and children's education costs I plan ahead. Can you please reverse the fee?",
      main_concerns: "Billing issue, Overdraft Fee",
      is_repeating_issue: false,
      was_issue_resolved: true,
      sentiment: -0.6,
    },
    {
      complaint_id: "SPRT_4",
      customer_id: "CUST_2",
      date: "02/11/2023",
      transcript:
        "I keep receiving notifications for 'low balance' alerts, even though I have over $25,000 in my account! I set the alert threshold much lower. It's annoying and makes me worry unnecessarily. Can you fix this? I've tried adjusting in the app, but it doesn't seem to save the changes. I need these alerts to be accurate for managing household and kids' expenses.",
      main_concerns: "Technical support, Account Alerts",
      is_repeating_issue: true,
      was_issue_resolved: false,
      sentiment: -0.4,
    },
  ],
}

// Concern options for the form
const CONCERN_OPTIONS = [
  "Billing issue",
  "Technical support",
  "Account Alerts",
  "Overdraft Fee",
  "Fraud concern",
  "Account access",
  "Card issue",
  "Transfer problem",
  "Loan question",
  "General inquiry",
]

interface CustomerSupportHistoryProps {
  customerId: string
}

export default function CustomerSupportHistory({ customerId }: CustomerSupportHistoryProps) {
  const { data: supportHistory, isLoading } = useCustomerSupportHistory(customerId);
  const [showForm, setShowForm] = useState(false)

  // Form state
  const [transcript, setTranscript] = useState<string>("")
  const [mainConcerns, setMainConcerns] = useState<string>("")
  const [isRepeatingIssue, setIsRepeatingIssue] = useState<boolean>(false)
  const [wasIssueResolved, setWasIssueResolved] = useState<boolean>(true)
  const [sentiment, setSentiment] = useState<number>(0)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    // Create new support record
    const newSupport = {
      complaint_id: `SPRT_${Math.floor(Math.random() * 1000)}`,
      customer_id: customerId,
      date: new Date().toLocaleDateString("en-GB"), // Format as DD/MM/YYYY
      transcript,
      main_concerns: mainConcerns,
      is_repeating_issue: isRepeatingIssue,
      was_issue_resolved: wasIssueResolved,
      sentiment: Number.parseFloat(sentiment.toFixed(1)),
    }

    // Reset form
    setTranscript("")
    setMainConcerns("")
    setIsRepeatingIssue(false)
    setWasIssueResolved(true)
    setSentiment(0)
    setShowForm(false)

    console.log("New support record added:", newSupport)
  }

  // Format date from DD/MM/YYYY to more readable format
  const formatDate = (dateString: string) => {
    const [day, month, year] = dateString.split("/")
    const date = new Date(`${year}-${month}-${day}`)
    return new Intl.DateTimeFormat("en-US", {
      day: "numeric",
      month: "short",
      year: "numeric",
    }).format(date)
  }

  // Get sentiment color based on value
  const getSentimentColor = (sentiment: number) => {
    if (sentiment >= 0.3) return "text-green-600"
    if (sentiment >= -0.3) return "text-amber-600"
    return "text-red-600"
  }

  // Get sentiment label based on value
  const getSentimentLabel = (sentiment: number) => {
    if (sentiment >= 0.7) return "Very Positive"
    if (sentiment >= 0.3) return "Positive"
    if (sentiment >= -0.3) return "Neutral"
    if (sentiment >= -0.7) return "Negative"
    return "Very Negative"
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Support History</CardTitle>
        <CardDescription>View and manage customer support interactions</CardDescription>
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <p className="text-center py-4">Loading support history...</p>
        ) : supportHistory ? (
          <div className="space-y-6">
            {supportHistory.map((support) => (
              <div key={support.complaint_id} className="border rounded-lg p-4 space-y-3">
                <div className="flex flex-wrap justify-between items-start gap-2">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium">{support.complaint_id}</span>
                      <span className="text-sm text-muted-foreground">{formatDate(support.date)}</span>
                    </div>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {support.main_concerns.map((concern: string, index: number) => (
                        <Badge key={index} variant="outline" className="text-xs">
                          {concern}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {support.is_repeating_issue && (
                      <div className="flex items-center text-amber-600 text-xs">
                        <RepeatIcon className="h-3.5 w-3.5 mr-1" />
                        Repeating Issue
                      </div>
                    )}
                    <div
                      className={`flex items-center text-xs ${support.was_issue_resolved ? "text-green-600" : "text-red-600"}`}
                    >
                      {support.was_issue_resolved ? (
                        <>
                          <CheckCircle2 className="h-3.5 w-3.5 mr-1" />
                          Resolved
                        </>
                      ) : (
                        <>
                          <AlertCircle className="h-3.5 w-3.5 mr-1" />
                          Unresolved
                        </>
                      )}
                    </div>
                    <div className={`flex items-center text-xs ${getSentimentColor(support.sentiment)}`}>
                      Sentiment: {getSentimentLabel(support.sentiment)}
                    </div>
                  </div>
                </div>

                <div className="bg-muted/50 p-3 rounded text-sm">
                  <p className="whitespace-pre-line">{support.transcript}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center py-4">No support history found for this customer.</p>
        )}

        {showForm && (
          <form onSubmit={handleSubmit} className="mt-6 space-y-4 border rounded-lg p-4">
            <h3 className="text-lg font-medium">Add New Support Record</h3>

            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="transcript">Transcript</Label>
                <Textarea
                  id="transcript"
                  value={transcript}
                  onChange={(e) => setTranscript(e.target.value)}
                  placeholder="Enter conversation transcript"
                  rows={4}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="mainConcerns">Main Concerns (comma separated)</Label>
                <Input
                  id="mainConcerns"
                  value={mainConcerns}
                  onChange={(e) => setMainConcerns(e.target.value)}
                  placeholder="e.g. Billing issue, Technical support"
                  required
                />
                <div className="flex flex-wrap gap-1 mt-1">
                  {CONCERN_OPTIONS.map((concern, index) => (
                    <Badge
                      key={index}
                      variant="outline"
                      className="text-xs cursor-pointer hover:bg-muted"
                      onClick={() => {
                        const concerns = mainConcerns.split(", ").filter((c) => c !== "")
                        if (!concerns.includes(concern)) {
                          setMainConcerns(concerns.length > 0 ? `${mainConcerns}, ${concern}` : concern)
                        }
                      }}
                    >
                      {concern}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <Switch id="isRepeatingIssue" checked={isRepeatingIssue} onCheckedChange={setIsRepeatingIssue} />
                <Label htmlFor="isRepeatingIssue">Repeating Issue</Label>
              </div>

              <div className="flex items-center space-x-2">
                <Switch id="wasIssueResolved" checked={wasIssueResolved} onCheckedChange={setWasIssueResolved} />
                <Label htmlFor="wasIssueResolved">Issue Resolved</Label>
              </div>

              <div className="space-y-2">
                <Label htmlFor="sentiment">Sentiment (-1.0 to 1.0)</Label>
                <div className="flex items-center gap-2">
                  <Input
                    id="sentiment"
                    type="range"
                    min="-1"
                    max="1"
                    step="0.1"
                    value={sentiment}
                    onChange={(e) => setSentiment(Number.parseFloat(e.target.value))}
                    className="w-full"
                  />
                  <span className={`text-sm font-medium ${getSentimentColor(sentiment)}`}>
                    {sentiment.toFixed(1)} ({getSentimentLabel(sentiment)})
                  </span>
                </div>
              </div>
            </div>

            <div className="flex justify-end space-x-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                Cancel
              </Button>
              <Button type="submit">Add Support Record</Button>
            </div>
          </form>
        )}
      </CardContent>
      <CardFooter className="flex justify-between">
        <div>
          {!isLoading && <span className="text-sm text-muted-foreground">{supportHistory?.length ?? 'No'} records found</span>}
        </div>
        {!showForm && <Button onClick={() => setShowForm(true)}>Add New Support Record</Button>}
      </CardFooter>
    </Card>
  )
}

