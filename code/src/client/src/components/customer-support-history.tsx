"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { AlertCircle, CheckCircle2, RepeatIcon } from "lucide-react"
import { useCustomerSupportHistory } from "@/lib/api"
import { formatDate } from "@/lib/utils"

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
        ) : supportHistory && "error" in supportHistory ?
          (
            <p className="text-center py-4">{supportHistory.error}</p>
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
    </Card>
  )
}

